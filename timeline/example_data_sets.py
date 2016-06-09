#!/usr/bin/env python3
# encoding: utf-8

import threading
import datetime
import time
import pandas as pd
import numpy as np
from data_sets import TimeSeries, LiveTimeSeries, TimeSeriesForecast


class LiveRandomData(LiveTimeSeries):
    def __init__(self):
        LiveTimeSeries.__init__(self, 'Live Random Time Series',
            'Random data which is generated on the fly.', 'live data')

        generator = threading.Thread(target=self.update_data)
        generator.daemon=True
        generator.start()

    def update_data(self, *args, **kwargs):
        mu = np.random.randint(0, 11)
        sigma = np.random.ranf() * 2
        while True:
            timestamp = datetime.datetime.now()
            data_point = sigma * np.random.randn() + mu
            with self.mutex:
                self.data[timestamp] = data_point
            time.sleep(1)

def generate_random_live_data_set():
    return LiveRandomData()

def generate_internet_traffic_forecast():
    data = pd.read_csv('../datasets/internet-traffic-data.csv',
        parse_dates='Time', index_col='Time')
    data = data / 8 / 2**30 # convert bits into GB
    data.rename(columns={'Internet traffic data (in bits)': 'GB'},
        inplace=True)

    training_set = data['GB'][:'2005-07-13 23:59:59'].copy()
    test_set = data['GB']['2005-07-14 00:00:00':].copy()
    forecast_data = data['2005-07-14 00:00:00':].copy()
    forecast_data.rename(columns={'GB': 'value'}, inplace=True)
    forecast_data['value'] = 0.5
    forecast_data['lower bound'] = forecast_data['value'] * 0.90
    forecast_data['upper bound'] = forecast_data['value'] * 1.10

    return TimeSeriesForecast('Internet Traffic Forecast', 'A exemplary \
        forecast of the internet traffic of a private ISP.', training_set,
        forecast_data, test_data=test_set, validation_split=1120780799)

def load_internet_traffic_data_set():
    data = pd.read_csv('../datasets/internet-traffic-data.csv',
        parse_dates='Time', index_col='Time')
    data = data / 8 / 2**30 # convert bits into GB
    data.rename(columns={'Internet traffic data (in bits)':
                         'Internet traffic data (in GB)'}, inplace=True)

    ts = data['Internet traffic data (in GB)']
    description = 'Internet traffic data (in GB) from a private ISP with \
        centres in 11 European cities. The data corresponds to a transatlantic \
        link and was collected from 06:57 hours on 7 June to 11:17 hours on 31 \
        July 2005. Data collected at five minute intervals.'

    return TimeSeries('Internet Traffic Data Set', description, ts,
        legend='traffic')

def generate_random_data_set(nsamples=1000):
    generate_random_data_set.counter += 1

    rng = pd.date_range('2010-01-01', periods=nsamples, freq='H')
    mu = np.random.randint(0, 11)
    sigma = np.random.ranf() * 2
    ts = pd.Series(sigma * np.random.randn(len(rng)) + mu, index=rng)

    name = 'Random Data Set {}'.format(generate_random_data_set.counter)
    description = 'Random data of {} samples, drawn from a normal distribution \
        with μ={} and σ={:.2f}'.format(nsamples, mu, sigma)

    return TimeSeries(name, description, ts, legend='random')

generate_random_data_set.counter = 0
