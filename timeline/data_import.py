#!/usr/bin/env python3
# encoding: utf-8

import threading
import time
import queue
import datetime

import pandas as pd
import numpy as np
import glob

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
            'name': 'live random time series',
            'legend': 'live data',
            'data': self.ts
        }

    def _data_generator(self):
        mu = np.random.randint(0, 11)
        sigma = np.random.ranf() * 2
        while True:
            data_point = sigma * np.random.randn() + mu
            self.queue.put((datetime.datetime.now(), data_point))
            time.sleep(1)

live_data = LiveRandomData()

class csvData:

    data = []

    def __init__(self, name, description, isForecast):
        self.name = name
        self.description = description
        self.isForecast = isForecast

    def add_data(self, data):
        self.data.append(data)

def get_data_set_from_folder():
    csvMap = {}
    counter = 0

    for fileName in glob.glob('../datasets/*.csv'):

        print(fileName)

        data = pd.read_csv(fileName, parse_dates='Time', index_col='Time', comment='#')
        data = data / 8 / 2**30 # convert bits into GB
        data.rename(columns={'Internet traffic data (in bits)':
                             'Internet traffic data (in GB)'}, inplace=True)

        i = 0
        with open(fileName) as f:
            for line in f:
                if line.startswith('#'):
                    comment = line.split(':')

                    if comment[0] == "#name":
                        name = comment[1]
                    elif comment[0] == "#description":
                        description = comment[1]
                    elif comment[0] == "#isForecast":
                        isForecast = comment[1]
                i += 1

        f.close()

        csv = csvData(name, description, isForecast)
        csv.add_data(data)

        csvMap[counter] = csv

        counter += 1

    j = 0
    while j < len(csvMap):
        print("DATA", j)
        print(csvMap[j].name)
        print(csvMap[j].description)
        print(csvMap[j].isForecast)
        print("--------------")
        j += 1

    return csvMap

def generate_random_data_set(nsamples=1000):
    generate_random_data_set.counter += 1
    rng = pd.date_range('2010-01-01', periods=nsamples, freq='H')
    mu = np.random.randint(0, 11)
    sigma = np.random.ranf() * 2
    ts = pd.Series(sigma * np.random.randn(len(rng)) + mu, index=rng)

    return {
        'name': 'random time series ' + str(generate_random_data_set.counter),
        'legend': 'random ' + str(generate_random_data_set.counter),
        'data': ts
    }

generate_random_data_set.counter = 0

def get_dummy_data_set():
    data = pd.read_csv('../datasets/internet-traffic-data.csv', parse_dates='Time', index_col='Time')
    data = data / 8 / 2**30 # convert bits into GB
    data.rename(columns={'Internet traffic data (in bits)':
                         'Internet traffic data (in GB)'}, inplace=True)
    return {
        'name': 'internet traffic data',
        'legend': 'traffic',
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
        'name': 'internet traffic forecast',
        'training_data': training_set,
        'validation_split': 1120780799,
        'true_forecast_data': real_data,
        'forecast_data': forecast_data
    }

def get_data_set(data_set_id):
    if data_set_id is None or data_set_id == 'random':
        return generate_random_data_set()
    if data_set_id == 'random_live':
        return live_data.get_data_set()
    return get_dummy_data_set()

def get_forecast(forecast_id):
    return get_dummy_forecast()
