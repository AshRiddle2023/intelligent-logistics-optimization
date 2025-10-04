# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def load_attachment2(file_path):
    """
    优化版数据加载函数
    读取附件2 Excel 文件并清洗
    """
    df = pd.read_excel(file_path)
    # 日期处理
    df['基准日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d', errors='coerce')
    df = df.dropna(subset=['基准日期'])
    
    # 提取发运时点（末4位数字）
    df['发运时点'] = df['线路编码'].str.extract(r'(\d{4})$')
    
    # 分钟偏移处理
    df['分钟偏移'] = pd.to_timedelta(df['分钟起始'].astype(str).str.split().str[0], errors='coerce')
    df = df.dropna(subset=['分钟偏移'])
    
    # 构建完整时间戳
    df['精确时间'] = df['基准日期'] + df['分钟偏移']
    
    # 周期特征
    df['周数'] = df['精确时间'].dt.isocalendar().week
    df['周几'] = df['精确时间'].dt.dayofweek + 1  # 1=周一
    df['时段类型'] = df['发运时点'].map({'0600':'早班','1400':'晚班'})
    
    # 过滤有效发运时段
    valid_data = df.query("发运时点 in ['0600','1400'] & 时段类型.notna()")
    
    return valid_data

def plot_dual_period(df):
    """
    双周期可视化
    输出 PDF：周维度趋势 + 日维度分布
    """
    plt.rcParams.update({'font.sans-serif': 'SimHei',
                         'axes.unicode_minus': False,
                         'figure.dpi': 300})
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), gridspec_kw={'height_ratios':[2,1]})
    
    # 周维度趋势
    sns.lineplot(data=df, x='周数', y='包裹量', hue='周几', style='时段类型',
                 markers=['o', 's'], palette='husl', ax=ax1)
    ax1.set_title('周维度货量趋势分析', fontsize=14, pad=12)
    ax1.set_xlabel('')
    
    # 日维度分布
    sns.boxplot(data=df, x='周几', y='包裹量', hue='时段类型', palette='Pastel2', ax=ax2)
    ax2.set_xticklabels(['周一','周二','周三','周四','周五','周六','周日'])
    ax2.set_title('日维度货量分布', fontsize=12, pad=10)
    
    plt.tight_layout()
    plt.savefig('双周期调度分析.pdf', bbox_inches='tight')
    print("可视化结果已保存至 双周期调度分析.pdf")

