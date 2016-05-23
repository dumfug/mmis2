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
        'data_col': 'Internet traffic data (in GB)',
        'data': data
    }
