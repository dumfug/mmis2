#!/usr/bin/env python3
# encoding: utf-8


def time_series_plot(data_set, **kwargs):
    data = _build_data_object(data_set['data'], data_set['data_col'])
    return {'title': data_set['name'], 'x_accessor': 'date',
      'y_accessor': 'value', 'data': [data], 'legend': ['data'], **kwargs}

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

def _build_data_object(data_set, collum):
    data = []
    for index, row in data_set.iterrows():
        data.append({
          'date': index.to_pydatetime().strftime('%s'),
          'value': row[collum]
        })
    return data
