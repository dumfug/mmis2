#!/usr/bin/env python3
# encoding: utf-8

import numpy as np


def time_series_plot(data_set, **kwargs):
    data = _build_data_object(data_set['data'])
    return {'title': data_set['name'], 'x_accessor': 'date',
            'y_accessor': 'value', 'data': [data], 'legend': ['data'],
            **kwargs}

def add_rolling_mean(data_set, viz, window):
    rolling_mean_ts = data_set['data'].rolling(window=window).mean().dropna()
    data = _build_data_object(rolling_mean_ts)
    viz['data'].append(data)
    viz['legend'].append('mean')

def add_rolling_std(data_set, viz, window):
    rolling_std_ts = data_set['data'].rolling(window=window).std().dropna()
    data = _build_data_object(rolling_std_ts)
    viz['data'].append(data)
    viz['legend'].append('std')

def auto_correlation_plot(data_set, max_lag, **kwargs):
    z95 = 1.959963984540054 # z-score for 0.95 of N(0,1)
    nsamples = len(data_set['data'])

    data = []
    for lag in range (max_lag):
        data.append({
            'lag': lag,
            'autocorrelation': data_set['data'].autocorr(lag),
            'plus95conf': z95 / np.sqrt(nsamples),
            'minus95conf': -z95 / np.sqrt(nsamples),
        })

    return {'title': 'ACF', 'data': data, 'x_accessor': 'lag',
            'y_accessor': ['autocorrelation', 'plus95conf', 'minus95conf'],
            'legend': ['autocorrelation', '+95% confidence', '-95% confidence'],
            'colors': ['#FF0000', '#333333', '#333333'], 'x_label': 'Lag',
            'y_label': 'Autocorrelation', 'baselines': [{'value': 0.0}],
            **kwargs}


def forecasting_eval_plot(model, **kwargs):
    training_data = _build_data_object(model['training_data'])

    forecast_data = []
    for index, row in model['forecast_data'].iterrows():
        forecast_data.append({
            'date': index.to_pydatetime().strftime('%s'),
            'value': row['value'],
            'lower': row['lower bound'],
            'upper': row['upper bound']
        })

    viz = {'title': model['name'], 'data': [training_data, forecast_data],
           'colors': ['#3C6662', '#D96C69'],
           'legend': ['training data', 'forecast'],
           'show_confidence_band': ['lower', 'upper']}

    if 'true_forecast_data' in model:
        real_data = _build_data_object(model['true_forecast_data'])
        viz['data'].append(real_data)
        viz['colors'].append('#6CBC67')
        viz['legend'].append('true forecast')

    if 'validation_split' in model:
        viz['markers'] = [{'date': model['validation_split'],
                           'label': 'validation split'}]

    return {**viz, **kwargs}

def _build_data_object(time_series):
    data = []
    for index, value in time_series.iteritems():
        data.append({
            'date': index.to_pydatetime().strftime('%s'),
            'value': value
        })
    return data
