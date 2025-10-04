# -*- coding: utf-8 -*-
import pandas as pd

def load_data():
    """
    加载数据，包括线路数据、站点数据、车队数据及预测结果
    """
    print("加载数据...")
    try:
        df_lines = pd.read_excel('data/附件1.xlsx')
        df_points = pd.read_excel('data/附件4.xlsx')
        df_fleet = pd.read_excel('data/附件5.xlsx')

        # 尝试读取新版本预测结果
        try:
            result_table1 = pd.read_excel('data/结果表1_new.xlsx')
            result_table2 = pd.read_excel('data/结果表2_new.xlsx')
        except:
            # 如果新版本不存在，读取原始版本
            result_table1 = pd.read_excel('data/结果表1.xlsx')
            result_table2 = pd.read_excel('data/结果表2.xlsx')

        return df_lines, df_points, df_fleet, result_table1, result_table2
    except Exception as e:
        print(f"加载数据时出错: {e}")
        return None, None, None, None, None

# -*- coding: utf-8 -*-
import re

def ensure_int(value, default=0):
    """
    将输入值转换为整数，失败时返回默认值
    """
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def extract_site_number(site_str):
    """
    从字符串中提取站点编号
    """
    if isinstance(site_str, str) and '站点' in site_str:
        try:
            return int(site_str.replace('站点',''))
        except ValueError:
            return None
    return None

def get_route_site_number(route):
    """
    从线路编码中提取站点编号
    """
    if isinstance(route, str):
        parts = route.split('- ')
        if len(parts) >= 2:
            return extract_site_number(parts[1])
    return None

def extract_departure_time(route_code):
    """
    从线路编码中提取发运时间（分钟数）
    """
    if isinstance(route_code, str):
        match = re.search(r'- (\d{4})$', route_code)
        if match:
            time_str = match.group(1)
            hours = int(time_str[:2])
            minutes = int(time_str[2:])
            return hours * 60 + minutes
    return None

