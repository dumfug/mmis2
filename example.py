#!/usr/bin/env python3
# encoding: utf-8

import timeline.app as app
import timeline.data_sets as data_sets
import timeline.example_data_sets as examples


def example():
    data_sets.register_data_set(examples.generate_random_data_set())
    data_sets.register_data_set(examples.generate_random_data_set())
    data_sets.register_data_set(examples.load_internet_traffic_data_set())
    data_sets.register_live_data_set(examples.generate_random_live_data_set())
    data_sets.register_forecast(examples.generate_internet_traffic_forecast())
    app.app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    example()
