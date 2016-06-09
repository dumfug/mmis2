#!/usr/bin/env python3
# encoding: utf-8

import numpy as np


def time_series_plot(data_sets, start_date=None, end_date=None, **kwargs):
    data = []
    legend = []

    if type(data_sets) != list:
        data_sets = [data_sets]

    for data_set in data_sets:
        ts = data_set.data if start_date is None else data_set.data[start_date:]
        ts = ts if end_date is None else ts[:end_date]
        data.append(build_data_object(ts))
        legend.append(data_set.legend)

    title = data_sets[0].name if len(data_sets) == 1 else ''

    return {'title': title, 'x_accessor': 'date', 'y_accessor': 'value',
            'data': data, 'legend': legend, **kwargs}

def add_rolling_mean(data_set, viz, window, start_date=None, end_date=None):
    ts = data_set.data if start_date is None else data_set.data[start_date:]
    ts = ts if end_date is None else ts[:end_date]

    rolling_mean_ts = ts.rolling(window=window).mean().dropna()
    data = build_data_object(rolling_mean_ts)
    viz['data'].append(data)
    viz['legend'].append('mean')

def add_rolling_std(data_set, viz, window, start_date=None, end_date=None):
    ts = data_set.data if start_date is None else data_set.data[start_date:]
    ts = ts if end_date is None else ts[:end_date]

    rolling_std_ts = ts.rolling(window=window).std().dropna()
    data = build_data_object(rolling_std_ts)
    viz['data'].append(data)
    viz['legend'].append('std')

def auto_correlation_plot(data_set, max_lag, **kwargs):
    z95 = 1.9599639845400540 # z-score for 0.95 of N(0,1)
    z99 = 2.5758293035489004 # z-score for 0.99 of N(0,1)
    nsamples = len(data_set.data)

    data = []
    for lag in range(1, max_lag):
        data.append({
            'lag': lag,
            'autocorrelation': data_set.data.autocorr(lag),
            'plus95conf': z95 / np.sqrt(nsamples),
            'plus99conf': z99 / np.sqrt(nsamples),
            'minus95conf': -z95 / np.sqrt(nsamples),
            'minus99conf': -z99 / np.sqrt(nsamples),
        })

    return {'title': 'ACF', 'data': data, 'x_accessor': 'lag',
            'y_accessor': ['autocorrelation', 'plus95conf', 'plus99conf',
            'minus95conf', 'minus99conf'], 'legend': ['autocorrelation',
            '+95% confidence', '+99% confidence', '-95% confidence',
            '-99% confidence'], 'colors': ['#DB4437', '#5C5C5C', '#3A3A3A',
            '#5C5C5C', '#3A3A3A'], 'x_label': 'Lag', 'y_label':
            'Autocorrelation', 'baselines': [{'value': 0.0}], **kwargs}

def forecasting_eval_plot(forecast, **kwargs):
    training_data = build_data_object(forecast.training_data)

    forecast_data = []
    for index, row in forecast.forcasted_data.iterrows():
        forecast_data.append({
            'date': index.to_pydatetime().strftime('%s'),
            'value': row['value'],
            'lower': row['lower bound'],
            'upper': row['upper bound']
        })

    viz = {'title': forecast.name, 'data': [training_data, forecast_data],
           'colors': ['#4040E8', '#DB4437'],
           'legend': ['training data', 'forecast'],
           'show_confidence_band': ['lower', 'upper']}

    if forecast.test_data is not None:
        test_data = build_data_object(forecast.test_data)
        viz['data'].append(test_data)
        viz['colors'].append('#05B378')
        viz['legend'].append('test data')

    if forecast.validation_split:
        viz['markers'] = [{'date': forecast.validation_split,
                           'label': 'validation split'}]

    return {**viz, **kwargs}

def build_data_object(time_series):
    data = []
    for index, value in time_series.iteritems():
        data.append({
            'date': index.to_pydatetime().strftime('%s'),
            'value': value
        })
    return data
