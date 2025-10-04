# -*- coding: utf-8 -*-
import pandas as pd

LOADING_TIME = 45
UNLOADING_TIME = 45
FIXED_COST_PER_DAY = 100

def assign_vehicles(transport_demands, df_lines, df_fleet, target_date):
    """
    分配车辆并计算成本
    """
    print("第三阶段：车辆分配...")

    fleet_info = {}
    for _, row in df_fleet.iterrows():
        fleet_info[row['车队编码']] = {
            'vehicles': row['自有车数量'],
            'vehicle_schedule': {}
        }

    line_info = {}
    for _, row in df_lines.iterrows():
        line_info[row['线路编码']] = {
            'travel_time': row['在途时长'],
            'own_cost': row['自有变动成本'],
            'external_cost': row['外部承运商成本']
        }

    scheduling_results = []

    for demand in transport_demands:
        routes = str(demand['route']).split(',') if ',' in str(demand['route']) else [demand['route']]
        primary_route = routes[0]
        departure_minute = demand['departure_minute']
        departure_time = demand['departure_time']
        fleet_code = demand['fleet_code']

        max_travel_time = max([line_info[r]['travel_time'] for r in routes if r in line_info] or [1.0])
        completion_minute = departure_minute + LOADING_TIME + max_travel_time * 2 * 60 + UNLOADING_TIME

        assigned_vehicle = None
        if fleet_code in fleet_info:
            fleet = fleet_info[fleet_code]
            for vehicle_id in range(1, fleet['vehicles'] + 1):
                vehicle_key = f"{fleet_code}-{vehicle_id}"
                if vehicle_key not in fleet['vehicle_schedule']:
                    assigned_vehicle = vehicle_key
                    fleet['vehicle_schedule'][vehicle_key] = []
                    break
                else:
                    last_task = fleet['vehicle_schedule'][vehicle_key][-1]
                    if last_task['completion_minute'] <= departure_minute:
                        assigned_vehicle = vehicle_key
                        break

        if assigned_vehicle:
            vehicle_type = "自有车"
            fleet['vehicle_schedule'][assigned_vehicle].append({
                'route': demand['route'],
                'departure_minute': departure_minute,
                'completion_minute': completion_minute
            })
            max_cost = max([line_info[r]['own_cost'] for r in routes if r in line_info] or [50])
            cost = max_cost
        else:
            vehicle_type = "外部"
            assigned_vehicle = "外部承运商"
            max_cost = max([line_info[r]['external_cost'] for r in routes if r in line_info] or [100])
            cost = max_cost

        scheduling_results.append({
            '线路编码': demand['route'],
            '日期': target_date,
            '预计发运时间': departure_time,
            '发运车辆': assigned_vehicle,
            '包裹量': demand['packages'],
            '成本': cost
        })

    return pd.DataFrame(scheduling_results)

# -*- coding: utf-8 -*-
FIXED_COST_PER_DAY = 100

def calculate_metrics(scheduling_results, df_fleet):
    """
    计算调度指标，包括自有车周转率、车辆均包裹量及总成本
    """
    print("计算调度指标...")

    total_own_vehicles = df_fleet['自有车数量'].sum()
    used_own_vehicles = set()
    external_vehicles = 0

    for _, row in scheduling_results.iterrows():
        if "外部" not in str(row['发运车辆']):
            used_own_vehicles.add(row['发运车辆'])
        else:
            external_vehicles += 1

    total_packages = scheduling_results['包裹量'].sum()
    vehicle_avg_packages = total_packages / (len(used_own_vehicles) + external_vehicles) if (len(used_own_vehicles) + external_vehicles) > 0 else 0
    own_fixed_cost = total_own_vehicles * FIXED_COST_PER_DAY
    total_cost = scheduling_results['成本'].sum() + own_fixed_cost
    own_vehicle_rotation_rate = len(used_own_vehicles) / total_own_vehicles if total_own_vehicles > 0 else 0

    metrics = {
        '自有车周转率': own_vehicle_rotation_rate,
        '车辆均包裹': vehicle_avg_packages,
        '总成本': total_cost,
        '自有车固定成本': own_fixed_cost,
        '运输成本': scheduling_results['成本'].sum(),
        '使用自有车数量': len(used_own_vehicles),
        '使用外部车数量': external_vehicles
    }

    return metrics
