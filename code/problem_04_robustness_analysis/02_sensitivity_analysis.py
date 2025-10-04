# -*- coding: utf-8 -*-
from src.data_loader import load_data
from src.dispatch_simulator import DispatchSimulator

def sensitivity_analysis():
    """
    对包裹量 ±10% 的扰动进行仿真，输出相对指标
    """
    df = load_data()
    simulator = DispatchSimulator()
    base_cost, base_turnover, base_load = simulator.run_simulation(df)

    scenarios = {
        '+10%': 1.1,
        '-10%': 0.9
    }

    results = {'基准': [100, 100, 100]}
    for scenario, ratio in scenarios.items():
        modified_df = df.copy()
        modified_df['包裹量'] *= ratio
        cost, turnover, load = simulator.run_simulation(modified_df)
        cost_rel = (cost / base_cost * 100) if base_cost !=0 else 0
        turnover_rel = (turnover / base_turnover * 100) if base_turnover !=0 else 0
        load_rel = (load / base_load * 100) if base_load !=0 else 0
        results[scenario] = [cost_rel, turnover_rel, load_rel]

    return results
