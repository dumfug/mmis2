# encoding: utf-8

import json
from datetime import datetime
from flask import Blueprint, request, Response, abort
from .data_sets import get_data_set, get_live_data_set, get_forecast
from .visualizations import (
    time_series_plot, add_rolling_mean, add_rolling_std, auto_correlation_plot,
    forecasting_eval_plot, build_data_object
)


api = Blueprint('api', __name__)

@api.route('/time_plot/<data_set_id>')
def time_plot(data_set_id):
    try:
        data_set = get_data_set(data_set_id)
    except KeyError:
        abort(404)

    start = datetime.fromtimestamp(int(request.args.get('start_date'))) \
        if 'start_date' in request.args else None
    end = datetime.fromtimestamp(int(request.args.get('end_date'))) \
        if 'end_date' in request.args else None

    viz = time_series_plot(data_set, start, end, area=False)

    if 'rolling_mean_window' in request.args:
        try:
            window = int(request.args.get('rolling_mean_window'))
            add_rolling_mean(data_set, viz, window, start, end)
        except ValueError:
            abort(400)

    if 'rolling_std_window' in request.args:
        try:
            window = int(request.args.get('rolling_std_window'))
            add_rolling_std(data_set, viz, window, start, end)
        except ValueError:
            abort(400)

    return Response(json.dumps(viz), mimetype='application/json')

@api.route('/time_plots')
def time_plots():
    try:
        data_sets = [get_data_set(id) for _, id in request.args.items()]
    except KeyError:
        abort(404)

    viz = time_series_plot(data_sets, area=False)
    return Response(json.dumps(viz), mimetype='application/json')

@api.route('/live_plot/<data_set_id>')
def live_plot(data_set_id):
    try:
        data_set = get_live_data_set(data_set_id)
    except KeyError:
        abort(404)

    if 'last_received' in request.args:
        # add 1 second offset to exclude the data from the last timestamp
        last_timestamp = int(request.args.get('last_received')) + 1
        start_date = datetime.fromtimestamp(last_timestamp)
        new_data = build_data_object(data_set.data[start_date:])
        return Response(json.dumps(new_data), mimetype='application/json')

    viz = time_series_plot(data_set, area=False)
    return Response(json.dumps(viz), mimetype='application/json')

@api.route('/acf_plot/<data_set_id>')
def acf_plot(data_set_id):
    try:
        data_set = get_data_set(data_set_id)
    except KeyError:
        abort(404)

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

@api.route('/forecasting_plot/<forecast_id>')
def forcasting_plot(forecast_id):
    try:
        forecast = get_forecast(forecast_id)
        print(forecast)
    except KeyError:
        abort(404)

    viz = forecasting_eval_plot(forecast, area=False)
    return Response(json.dumps(viz), mimetype='application/json')
