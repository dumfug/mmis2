# encoding: utf-8

import json
from datetime import datetime
from flask import Blueprint, request, Response, abort
from data_import import get_data_set, get_live_data_set, get_forecast_data_set
from visualizations import (
    time_series_plot, add_rolling_mean, add_rolling_std, auto_correlation_plot,
    forecasting_eval_plot, build_data_object
)


api = Blueprint('api', __name__)

@api.route('/time_plot', defaults={'data_set_id': 'random'})
@api.route('/time_plot/<data_set_id>')
def time_plot(data_set_id):
    # TODO: error handling for invalid data set id
    data_set = get_data_set(data_set_id)

    if request.args.get('start_date', None):
        start = datetime.fromtimestamp(int(request.args.get('start_date')))
        data_set['data'] = data_set['data'][start:]

    if request.args.get('end_date', None):
        end = datetime.fromtimestamp(int(request.args.get('end_date')))
        data_set['data'] = data_set['data'][:end]

    viz = time_series_plot(data_set, area=False)

    if request.args.get('rolling_mean_window', None):
        try:
            window = int(request.args.get('rolling_mean_window'))
            add_rolling_mean(data_set, viz=viz, window=window)
        except ValueError:
            abort(400)

    if request.args.get('rolling_std_window', None):
        try:
            window = int(request.args.get('rolling_std_window'))
            add_rolling_std(data_set, viz=viz, window=window)
        except ValueError:
            abort(400)

    return Response(json.dumps(viz), mimetype='application/json')

@api.route('/time_plots')
def time_plots():
    # TODO: error handling for invalid data set ids
    data_sets = [get_data_set(id) for _, id in request.args.items()]
    viz = time_series_plot(data_sets, area=False)
    return Response(json.dumps(viz), mimetype='application/json')

@api.route('/live_plot', defaults={'data_set_id': 'random_live'})
@api.route('/live_plot/<data_set_id>')
def live_plot(data_set_id):
    data_set = get_live_data_set(data_set_id)

    if request.args.get('last_received', None):
        last_timestamp = int(request.args.get('last_received'))
        # add 1 second offset to exclude the data from the last time stamp
        start_date = datetime.fromtimestamp(last_timestamp + 1)
        new_data = build_data_object(data_set['data'][start_date:])
        return Response(json.dumps(new_data), mimetype='application/json')

    viz = time_series_plot(data_set, area=False)
    return Response(json.dumps(viz), mimetype='application/json')

@api.route('/acf_plot/<data_set_id>')
def acf_plot(data_set_id):
    data_set = get_data_set(data_set_id)

    try:
        max_lag = int(request.args.get('max_lag', ''))
        if max_lag <= 0:
            raise ValueError
    except ValueError:
        abort(400)

    viz = auto_correlation_plot(data_set, max_lag, left=100, area=False)

    if request.args.get('scale', '').lower() in ['true', 't', 'yes', 'y', '1']:
        viz.update({'min_y': -1, 'max_y': +1})

    return Response(json.dumps(viz), mimetype='application/json')

@api.route('/forecasting_plot/<int:forecast_id>')
def forcasting_plot(forecast_id):
    forecast = get_forecast_data_set(forecast_id)
    viz = forecasting_eval_plot(forecast, area=False)
    return Response(json.dumps(viz), mimetype='application/json')
