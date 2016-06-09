#!/usr/bin/env python3
# encoding: utf-8

from flask import Flask
from frontend import frontend
from api import api
import example_data_sets as examples
import data_sets


app = Flask(__name__)
app.register_blueprint(frontend)
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    data_sets.register_data_set(examples.generate_random_data_set())
    data_sets.register_data_set(examples.generate_random_data_set())
    data_sets.register_data_set(examples.load_internet_traffic_data_set())
    data_sets.register_live_data_set(examples.generate_random_live_data_set())
    data_sets.register_forecast(examples.generate_internet_traffic_forecast())

    app.run(host='0.0.0.0', debug=True)
