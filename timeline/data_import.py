#!/usr/bin/env python3
# encoding: utf-8

import threading
import time
import queue
import datetime

import pandas as pd
import numpy as np


class LiveRandomData(object):
    def __init__(self):
        self.ts = pd.Series()
        self.queue = queue.Queue()

        generator = threading.Thread(target=self._data_generator)
        generator.daemon=True
        generator.start()

    def get_data_set(self):
        while True:
            try:
                time_stamp, data = self.queue.get(block=False)
                self.ts[time_stamp] = data
            except queue.Empty:
                break

        return {
            'id': 0,
            'name': 'Live Random Time Series',
            'legend': 'live data',
            'description': 'Random data which is generated on the fly.',
            'data': self.ts
        }

    def _data_generator(self):
        mu = np.random.randint(0, 11)
        sigma = np.random.ranf() * 2
        while True:
            data_point = sigma * np.random.randn() + mu
            self.queue.put((datetime.datetime.now(), data_point))
            time.sleep(1)

live_random_data = LiveRandomData()

def generate_random_data_set(nsamples=1000):
    generate_random_data_set.counter += 1
    rng = pd.date_range('2010-01-01', periods=nsamples, freq='H')
    mu = np.random.randint(0, 11)
    sigma = np.random.ranf() * 2
    ts = pd.Series(sigma * np.random.randn(len(rng)) + mu, index=rng)

    return {
        'id': 'random' + str(generate_random_data_set.counter),
        'name': 'Random Time Series Data Set ' + str(generate_random_data_set.counter),
        'legend': 'random ' + str(generate_random_data_set.counter),
        'description': 'Random data with ... samples, drawn from a normal distribution with mu={} and std={:.2f}'.format(mu, sigma),
        'data': ts
    }

generate_random_data_set.counter = 0

def get_dummy_data_set():
    data = pd.read_csv('../datasets/internet-traffic-data.csv', parse_dates='Time', index_col='Time')
    data = data / 8 / 2**30 # convert bits into GB
    data.rename(columns={'Internet traffic data (in bits)':
                         'Internet traffic data (in GB)'}, inplace=True)
    return {
        'id': 0,
        'name': 'Internet Traffic Data Set',
        'legend': 'traffic',
        'description': 'Internet traffic data (in GB) from a private ISP with centres in 11 European cities. The data corresponds to a transatlantic link and was collected from 06:57 hours on 7 June to 11:17 hours on 31 July 2005. Data collected at five minute intervals.',
        'data': data['Internet traffic data (in GB)']
    }

def get_dummy_forecast():
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
        'id': 0,
        'name': 'internet traffic forecast',
        'description': 'Forecast description.',
        'training_data': training_set,
        'validation_split': 1120780799,
        'true_forecast_data': real_data,
        'forecast_data': forecast_data
    }

def get_data_set(data_set_id):
    if data_set_id is None or data_set_id == 'random':
        return generate_random_data_set()
    return get_dummy_data_set()

def get_live_data_set(data_set_id):
    return live_random_data.get_data_set()

def get_forecast_data_set(forecast_id):
    return get_dummy_forecast()

def get_all_data_sets():
    return [get_dummy_data_set(), generate_random_data_set()]

def get_all_live_data_sets():
    return [live_random_data.get_data_set()]

def get_all_eval_forecast_data_sets():
    return [get_dummy_forecast()]
