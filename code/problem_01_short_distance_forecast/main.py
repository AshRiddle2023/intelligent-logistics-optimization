# -*- coding: utf-8 -*-
from pathlib import Path
from code.problem_01_short_distance_forecast.01_data_preprocessing import load_attachment2, plot_dual_period
from code.problem_01_short_distance_forecast.02_forecasting_sarima_lstm import EnhancedFreightPredictor
from code.problem_01_short_distance_forecast.03_result_generator import ResultGenerator
from code.problem_01_short_distance_forecast.04_visualization import plot_distribution

# 数据加载
file_path = Path("../data/附件2.xlsx")
df = load_attachment2(file_path)
plot_dual_period(df)

# 预测准备
hist_data = df
preknown_data = {'场地3-站点83-0600':1850, '场地3-站点83-1400':2120}

predictor = EnhancedFreightPredictor(hist_data, preknown_data)

results = []
for line in preknown_data.keys():
    pred = predictor.predict(line, '2023-12-15')
    results.append({'线路编码':line, '总货量':pred.sum(), '时段分布':pred})

# 生成结果表
result_generator = ResultGenerator('2023-12-15 14:00')
table1 = result_generator.generate_table1(results)
table2 = result_generator.generate_table2(results)

# 可视化
for res in results:
    plot_distribution(res['线路编码'], res['时段分布'])
