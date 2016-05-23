#!/usr/bin/env python3
# encoding: utf-8


def time_series_plot(data_set, **kwargs):
    data = []
    for index, row in data_set['data'].iterrows():
        data.append({
          'date': index.to_pydatetime().strftime('%s'),
          'value': row[data_set['data_col']]
        })

    return {'title': data_set['name'], 'data': data, **kwargs}
