# -*- coding: utf-8 -*-
import time
from src.data_loader import load_data
from src.graph_operations import create_string_points_graph, get_string_point_sets
from src.transport_demand import generate_transport_demands
from src.string_point_optimizer import optimize_string_points
from src.vehicle_assignment import assign_vehicles
from src.metrics import calculate_metrics

start_time = time.time()

def main():
    df_lines, df_points, df_fleet, result_table1, result_table2 = load_data()
    if df_lines is None:
        print("数据加载失败，程序退出")
        return

    global target_date
    target_date = result_table1['日期'].iloc[0]

    string_points_graph = create_string_points_graph(df_points)
    string_point_sets = get_string_point_sets(string_points_graph)
    print(f"找到{len(string_point_sets)}个可串点集合")

    transport_demands = generate_transport_demands(df_lines, result_table1, result_table2)
    print(f"生成{len(transport_demands)}个初始运输需求")

    optimized_demands = optimize_string_points(transport_demands, string_point_sets)
    print(f"优化后{len(optimized_demands)}个运输需求")

    scheduling_results = assign_vehicles(optimized_demands, df_lines, df_fleet, target_date)
    metrics = calculate_metrics(scheduling_results, df_fleet)

    scheduling_results.to_excel('results/结果表3.xlsx', index=False)
    scheduling_results.to_csv('results/结果表3.csv', index=False)
    print("调度结果已保存到 results 文件夹")

    print("\n调度指标:")
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")

    end_time = time.time()
    print(f"\n总运行时间: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main()
