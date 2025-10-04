# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_distribution(line_code, pred_data):
    time_points = pd.date_range('2023-12-15 14:00','2023-12-16 14:00', freq='10T', inclusive='left')
    plt.figure(figsize=(18,6))
    plt.bar(time_points, pred_data, width=0.015)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))
    plt.xlim([pd.Timestamp('2023-12-15 13:30'), pd.Timestamp('2023-12-16 14:30')])
    plt.title(f'{line_code} 货量分布预测 (2023-12-15 14:00 至 2023-12-16 14:00)')
    plt.xlabel('时间')
    plt.ylabel('包裹量')
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
