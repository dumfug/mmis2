#!/usr/bin/env python3
# encoding: utf-8

import numpy as np


def time_series_plot(data_set, **kwargs):
    data = _build_data_object(data_set['data'], data_set['data_col'])
    return {'title': data_set['name'], 'x_accessor': 'date',
            'y_accessor': 'value', 'data': [data], 'legend': ['data'],
            **kwargs}

def add_rolling_mean(data_set, collum, viz, window):
    rolling_mean_ts = data_set['data'].rolling(window=window).mean().dropna()
    data = _build_data_object(rolling_mean_ts, collum)
    viz['data'].append(data)
    viz['legend'].append('mean')

def add_rolling_std(data_set, collum, viz, window):
    rolling_std_ts = data_set['data'].rolling(window=window).std().dropna()
    data = _build_data_object(rolling_std_ts, collum)
    viz['data'].append(data)
    viz['legend'].append('std')

def auto_correlation_plot(data_set, max_lag, **kwargs):
    z95 = 1.959963984540054 # z-score for 0.95 of N(0,1)
    time_series = data_set['data']['Internet traffic data (in GB)']

    data = []
    for lag in range (max_lag):
        data.append({
            'lag': lag,
            'autocorrelation': time_series.autocorr(lag),
            'plus95conf': z95 / np.sqrt(len(time_series)),
            'minus95conf': -z95 / np.sqrt(len(time_series)),
        })

    return {'title': 'ACF', 'data': data, 'x_accessor': 'lag',
            'y_accessor': ['autocorrelation', 'plus95conf', 'minus95conf'],
            'legend': ['autocorrelation', '+95% confidence', '-95% confidence'],
            'colors': ['#FF0000', '#333333', '#333333'], 'x_label': 'Lag',
            'y_label': 'Autocorrelation', 'baselines': [{'value': 0.0}],
            **kwargs}

def _build_data_object(data_set, collum):
    data = []
    for index, row in data_set.iterrows():
        data.append({
            'date': index.to_pydatetime().strftime('%s'),
            'value': row[collum]
        })
    return data
