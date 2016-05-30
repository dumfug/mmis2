#!/usr/bin/env python3
# encoding: utf-8

import pandas as pd


def get_dummy_data_set():
    data = pd.read_csv('../datasets/internet-traffic-data.csv', parse_dates='Time', index_col='Time')
    data = data / 8 / 2**30 # convert bits into GB
    data.rename(columns={'Internet traffic data (in bits)':
                         'Internet traffic data (in GB)'}, inplace=True)
    return {
        'name': 'internet traffic data',
        'data': data['Internet traffic data (in GB)']
    }

def get_dummy_model():
    data = pd.read_csv('../datasets/internet-traffic-data.csv', parse_dates='Time', index_col='Time')
    data = data / 8 / 2**30 # convert bits into GB
    data.rename(columns={'Internet traffic data (in bits)':
                         'Internet traffic data (in GB)'}, inplace=True)

    training_set = data['Internet traffic data (in GB)'][:'2005-07-13 23:59:59'].copy()

    real_data = data['Internet traffic data (in GB)']['2005-07-14 00:00:00':].copy()

    forecast_data = data['2005-07-14 00:00:00':].copy()
    forecast_data.rename(columns={'Internet traffic data (in GB)': 'value'}, inplace=True)
    forecast_data['value'] = 0.5
    forecast_data['lower bound'] = forecast_data['value'] * 0.90
    forecast_data['upper bound'] = forecast_data['value'] * 1.10

    return {
        'name': 'internet traffic forecast',
        'training_data': training_set,
        'validation_split': 1120780799,
        'true_forecast_data': real_data,
        'forecast_data': forecast_data
    }

def get_data_set(data_set_id):
    return get_dummy_data_set()

def get_model(model_id):
    return get_dummy_model()
