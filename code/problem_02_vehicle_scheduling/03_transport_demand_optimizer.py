# -*- coding: utf-8 -*-
import pandas as pd
from src.utils import ensure_int, get_route_site_number

VEHICLE_CAPACITY = 1000
LOADING_TIME = 45
UNLOADING_TIME = 45

def generate_transport_demands(df_lines, result_table1, result_table2):
    """
    基于预测货量生成初始运输需求
    """
    print("第一阶段：生成初始运输需求...")
    transport_demands = []
    target_date = result_table1['日期'].iloc[0]

    for _, row in result_table1.iterrows():
        route = row['线路编码']
        total_packages = row['货量']
        if pd.isna(total_packages) or total_packages <= 0:
            continue

        route_packages = result_table2[(result_table2['线路编码'] == route) &
                                       (result_table2['日期'] == target_date)].sort_values('分钟起始')
        route_info = df_lines[df_lines['线路编码'] == route]
        if route_info.empty:
            print(f"警告: 找不到线路 {route} 的信息")
            continue

        fleet_code = route_info['车队编码'].values[0]

        # 确定发运时间
        departure_time = None
        if "0600" in str(route):
            departure_time = 6 * 60
        elif "1400" in str(route):
            departure_time = 14 * 60
        else:
            try:
                node_time = route_info['发运节点'].values[0]
                if isinstance(node_time, float):
                    hours = int(node_time * 24)
                    minutes = int((node_time * 24 * 60) % 60)
                    departure_time = hours * 60 + minutes
            except:
                pass
        if departure_time is None:
            departure_time = 6 * 60

        accumulated_packages = 0
        last_minute = 0

        if not route_packages.empty:
            for _, pkg_row in route_packages.iterrows():
                minute = ensure_int(pkg_row['分钟起始'])
                packages = pkg_row['包裹量']
                if pd.isna(packages) or packages <= 0:
                    continue
                accumulated_packages += packages
                last_minute = minute
                if accumulated_packages >= VEHICLE_CAPACITY:
                    vehicles_needed = int(accumulated_packages / VEHICLE_CAPACITY)
                    remaining_packages = accumulated_packages % VEHICLE_CAPACITY
                    for _ in range(vehicles_needed):
                        hours = int(departure_time / 60)
                        mins = int(departure_time % 60)
                        departure_time_str = f"{hours:02d}:{mins:02d}"
                        transport_demands.append({
                            'route': route,
                            'packages': VEHICLE_CAPACITY,
                            'departure_minute': departure_time,
                            'departure_time': departure_time_str,
                            'fleet_code': fleet_code,
                            'is_full': True,
                            'site_number': get_route_site_number(route)
                        })
                    accumulated_packages = remaining_packages
        else:
            vehicles_needed = int(total_packages / VEHICLE_CAPACITY)
            remaining_packages = total_packages % VEHICLE_CAPACITY
            for _ in range(vehicles_needed):
                hours = int(departure_time / 60)
                mins = int(departure_time % 60)
                departure_time_str = f"{hours:02d}:{mins:02d}"
                transport_demands.append({
                    'route': route,
                    'packages': VEHICLE_CAPACITY,
                    'departure_minute': departure_time,
                    'departure_time': departure_time_str,
                    'fleet_code': fleet_code,
                    'is_full': True,
                    'site_number': get_route_site_number(route)
                })
            if remaining_packages > 0:
                hours = int(departure_time / 60)
                mins = int(departure_time % 60)
                departure_time_str = f"{hours:02d}:{mins:02d}"
                transport_demands.append({
                    'route': route,
                    'packages': remaining_packages,
                    'departure_minute': departure_time,
                    'departure_time': departure_time_str,
                    'fleet_code': fleet_code,
                    'is_full': False,
                    'site_number': get_route_site_number(route)
                })

    return transport_demands

# -*- coding: utf-8 -*-
from src.utils import get_route_site_number

MAX_STRING_POINTS = 3
VEHICLE_CAPACITY = 1000

def optimize_string_points(transport_demands, string_point_sets):
    """
    将部分装载的运输需求进行串点优化
    """
    print("第二阶段：串点优化...")
    partial_demands = [d for d in transport_demands if not d['is_full']]
    full_demands = [d for d in transport_demands if d['is_full']]

    grouped_demands = {}
    for demand in partial_demands:
        if isinstance(demand['route'], str):
            route_parts = demand['route'].split('- ')
            start_site = route_parts[0] if len(route_parts) > 0 else None
            departure_time = demand['departure_time']
            fleet_code = demand['fleet_code']
            key = (start_site, departure_time, fleet_code)
            grouped_demands.setdefault(key, []).append(demand)

    optimized_demands = []

    for key, demands in grouped_demands.items():
        if len(demands) == 1:
            optimized_demands.append(demands[0])
            continue
        demands.sort(key=lambda x: x['packages'], reverse=True)

        while demands:
            base_demand = demands.pop(0)
            base_site = base_demand['site_number']
            combined_routes = [base_demand['route']]
            combined_packages = base_demand['packages']
            combined_sites = [base_site] if base_site is not None else []

            i = 0
            while i < len(demands) and len(combined_routes) < MAX_STRING_POINTS:
                current_demand = demands[i]
                current_site = current_demand['site_number']
                can_string = False
                if base_site is not None and current_site is not None:
                    for point_set in string_point_sets:
                        if base_site in point_set and current_site in point_set:
                            can_string = True
                            break
                if can_string and combined_packages + current_demand['packages'] <= VEHICLE_CAPACITY:
                    combined_routes.append(current_demand['route'])
                    combined_packages += current_demand['packages']
                    combined_sites.append(current_site)
                    demands.pop(i)
                else:
                    i += 1

            optimized_demands.append({
                'route': ','.join(combined_routes),
                'packages': combined_packages,
                'departure_minute': base_demand['departure_minute'],
                'departure_time': base_demand['departure_time'],
                'fleet_code': base_demand['fleet_code'],
                'is_full': combined_packages >= VEHICLE_CAPACITY * 0.9,
                'site_number': base_site,
                'string_points': combined_sites if len(combined_sites) > 0 else None
            })

    final_demands = full_demands + optimized_demands
    final_demands.sort(key=lambda x: x['departure_minute'])
    return final_demands
