# encoding: utf-8

from flask import Blueprint, render_template
from data_sets import (
    get_data_set, get_live_data_set, get_forecast, get_all_data_sets,
    get_all_live_data_sets, get_all_forecasts
)

frontend = Blueprint('profile', __name__)


@frontend.route('/test')
def test():
    return render_template('test.html')

@frontend.route('/info/<data_set_id>')
def info(data_set_id):
    return render_template(
        'info.html',
        data_set=get_data_set(data_set_id)
    )

@frontend.route('/multi_time_plots')
def multi_time_plots():
    return render_template(
        'multi_time_plots.html',
        data_sets=get_all_data_sets())

@frontend.route('/live_info/<data_set_id>')
def live_info(data_set_id):
    return render_template(
        'live_info.html',
        data_set=get_live_data_set(data_set_id)
    )

@frontend.route('/eval_info/<data_set_id>')
def eval_info(data_set_id):
    return render_template(
        'eval_info.html',
        data_set=get_forecast(data_set_id)
    )

@frontend.route('/')
def index():
    return render_template(
        'index.html',
        data_sets=get_all_data_sets(),
        live_data_sets=get_all_live_data_sets(),
        eval_data_sets=get_all_forecasts()
    )
