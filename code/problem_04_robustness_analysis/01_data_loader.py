# -*- coding: utf-8 -*-
import pandas as pd
from datetime import timedelta

# 文件路径配置
DATA_PATH = "C:/Users/###/Downloads/附件3.xlsx"

def load_data():
    """
    读取原始数据，并进行时间增强、列名标准化及包裹量处理
    """
    try:
        df = pd.read_excel(DATA_PATH)
        # 列名标准化
        df.columns = df.columns.str.strip().str.replace(r'[\s_]+', '', regex=True)
        # 时间处理增强（支持分钟起始的多种格式）
        if '分钟起始' not in df.columns:
            if '时间分钟' in df.columns:
                df.rename(columns={'时间分钟':'分钟起始'}, inplace=True)
            else:
                df['分钟起始'] = [timedelta(hours=8) + timedelta(minutes=15*i) for i in range(len(df))]
        # 数据类型转换
        df['日期'] = pd.to_datetime(df['日期'])
        df['分钟起始'] = pd.to_timedelta(df['分钟起始'].astype(str))
        df['时间戳'] = df['日期'] + df['分钟起始']  # 关键字段
        df['包裹量'] = df['包裹量'].clip(lower=0.1).astype(float)
        return df
    except Exception as e:
        print(f"数据加载错误: {str(e)}")
        exit()

# -*- coding: utf-8 -*-
import numpy as np

class DispatchSimulator:
    """增强调度仿真器"""
    def __init__(self, buffer_ratio=0.15):
        self.buffer_ratio = buffer_ratio
        self.vehicle_pool = {
            'A': {'capacity': 1000, 'count': 15, 'cost': 800},
            'B': {'capacity': 800, 'count': 20, 'cost': 600},
            'C': {'capacity': 1500, 'count': 10, 'cost': 1000}
        }

    def _safe_divide(self, a, b):
        return a / b if b != 0 else 0

    def run_simulation(self, df):
        """
        核心调度逻辑：
        - 总成本计算
        - 车辆周转率
        - 车辆均载量
        """
        try:
            total_packages = df['包裹量'].sum()
            base_cost = total_packages * 0.8
            buffer_cost = total_packages * self.buffer_ratio * 0.6
            total_cost = base_cost + buffer_cost

            used_vehicles = np.ceil(total_packages / 1000)
            total_vehicles = sum(v['count'] for v in self.vehicle_pool.values())
            turnover_rate = self._safe_divide(used_vehicles, total_vehicles)

            avg_load = self._safe_divide(total_packages, used_vehicles)
            return total_cost, turnover_rate, avg_load
        except Exception as e:
            print(f"仿真错误: {str(e)}")
            return 0, 0, 0

