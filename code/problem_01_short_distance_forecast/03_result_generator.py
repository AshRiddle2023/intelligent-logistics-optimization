# -*- coding: utf-8 -*-
import pandas as pd

class ResultGenerator:
    def __init__(self, start_datetime):
        self.time_points = pd.date_range(start_datetime, periods=144, freq='10T')

    def generate_table1(self, predictions):
        return pd.DataFrame(columns=['线路编码', '日期', '货量'])

    def generate_table2(self, predictions):
        return pd.DataFrame(columns=['线路编码','日期','分钟起始','包裹量'])
