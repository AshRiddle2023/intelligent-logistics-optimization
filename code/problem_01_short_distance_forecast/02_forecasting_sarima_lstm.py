# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.cluster import KMeans
from scipy.ndimage import gaussian_filter

class EnhancedFreightPredictor:
    def __init__(self, hist_data, preknown_data):
        self.hist = self._enhanced_preprocess(hist_data)
        self.preknown = preknown_data
        self.time_bins = pd.date_range('2023-12-15 14:00', '2023-12-16 14:00', freq='10T', inclusive='left').time
        self.templates = self._build_enhanced_templates()

    def _enhanced_preprocess(self, data):
        data['datetime'] = pd.to_datetime(data['日期'])
        data['发运时点'] = data['线路编码'].str[-4:]
        data['小时段'] = data['datetime'].dt.floor('10T').dt.time
        data['工作日'] = data['datetime'].dt.weekday < 5
        return data[['线路编码','datetime','发运时点','包裹量','小时段','工作日']]

    def _build_enhanced_templates(self):
        templates = {}
        for line in self.hist['线路编码'].unique():
            line_data = self.hist[self.hist['线路编码']==line]
            time_matrix = line_data.pivot_table(
                index='datetime', columns='小时段', values='包裹量', aggfunc='sum', fill_value=0
            ).reindex(columns=self.time_bins, fill_value=0)
            
            smoothed = gaussian_filter(time_matrix.values.astype(float), sigma=1.2)
            
            if len(time_matrix) >= 3:
                kmeans = KMeans(n_clusters=2, random_state=42).fit(smoothed)
                template = kmeans.cluster_centers_.max(axis=0)
            else:
                template = smoothed.mean(axis=0)
            
            templates[line] = template / template.sum()
        return templates

    def _dynamic_adjustment(self, line_code, base_pred):
        line_data = self.hist[self.hist['线路编码']==line_code]
        hour_dist = line_data.groupby('小时段')['包裹量'].mean()
        combined = 0.6*self.templates[line_code] + 0.4*hour_dist.reindex(self.time_bins, fill_value=0.01).values
        return base_pred * combined / combined.sum()

    def predict(self, line_code, predict_date):
        ts = self.hist[self.hist['线路编码']==line_code].groupby('datetime')['包裹量'].sum()
        if len(ts) > 5:
            try:
                model = SARIMAX(ts, order=(1,0,1), seasonal_order=(1,1,1,7)).fit(disp=False)
                base_pred = model.forecast(steps=1).values[0]
            except:
                base_pred = ts.ewm(span=3).mean().iloc[-1]
        else:
            base_pred = ts.mean() if not ts.empty else self.preknown.get(line_code, 1000)
        
        final_pred = 0.7*self.preknown.get(line_code, base_pred) + 0.3*base_pred
        detailed = self._dynamic_adjustment(line_code, final_pred).astype(int)

        peak_hours = [(7,9),(17,19)]
        for i,t in enumerate(self.time_bins):
            if any(start <= t.hour < end for start,end in peak_hours):
                detailed[i] = max(detailed[i],0)
            else:
                detailed[i] = 0 if detailed[i]<5 else detailed[i]
        detailed *= int(final_pred/detailed.sum())
        return detailed
