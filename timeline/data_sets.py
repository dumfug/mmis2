#!/usr/bin/env python3
# encoding: utf-8

import uuid
from threading import Lock
import pandas as pd


forecasts = dict()
time_series = dict()
live_time_series = dict()

def register_data_set(data_set):
    time_series[data_set.id] = data_set

def register_live_data_set(data_set):
    live_time_series[data_set.id] = data_set

def register_forecast(forecast):
    forecasts[forecast.id] = forecast

def get_data_set(data_set_id):
    ts = time_series.get(data_set_id)
    if not ts:
        raise KeyError('No data set with such ID.')
    return ts

def get_live_data_set(data_set_id):
    ts = live_time_series.get(data_set_id)
    if not ts:
        raise KeyError('No live data set with such ID.')
    return ts

def get_forecast(forecast_id):
    forecast = forecasts.get(forecast_id)
    if not forecast:
        raise KeyError('No forecast with such ID.')
    return forecast

def get_all_data_sets():
    return time_series.values()

def get_all_live_data_sets():
    return live_time_series.values()

def get_all_forecasts():
    return forecasts.values()

class TimeSeries(object):
    def __init__(self, name, description, ts, legend=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.data = ts
        self.legend = name if legend is None else legend

    @property
    def number_of_samples(self):
        return len(self.data)

    @property
    def start_date(self):
        return self.data.keys()[0]

    @property
    def end_date(self):
        return self.data.keys()[-1]

    @property
    def period(self):
        firstPeriod = self.data.keys()[1] - self.data.keys()[0]
        i = 1

        while i < len(self.data.keys()) - 1:
            period = self.data.keys()[i + 1] - self.data.keys()[i]
            i += 1

            if period != firstPeriod:
                return "non periodic"

        return period

class LiveTimeSeries(TimeSeries):
    def __init__(self, name, description, legend=None):
        TimeSeries.__init__(self, name, description, pd.Series(), legend=legend)
        self.mutex = Lock()

    def get_data(self, start=None, end=None):
        with self.mutex:
            ts = self.data if start is None else self.data[start:]
            ts = ts if end is None else ts[:end]
            return ts

    def update_data(self, *args, **kwargs):
        raise NotImplementedError

class TimeSeriesForecast(TimeSeries):
    def __init__(self, name, description, training_data, forcasted_data,
                 test_data=None, validation_split=None):
        TimeSeries.__init__(self, name, description, training_data, '.legend')
        self.training_data = training_data
        self.forcasted_data = forcasted_data
        self.test_data = test_data
        self.validation_split = validation_split
