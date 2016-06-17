var intervalId;
var live_params;
var data;
var last_date;
var live_viz;

function time_plot(target_id, params) {
    show_empty_plot(target_id, 'loading');

    $.getJSON($SCRIPT_ROOT + '/api/time_plot/' + params.id, params, function(viz) {
        convert_data_array(viz);

        viz.full_width = true;
        viz.height = 400;
        viz.right = 40;
        viz.target = target_id;

        MG.data_graphic(viz);
    }).fail(function() {
        show_empty_plot(target_id, 'sorry, an error occurred');
    });
};

function multiple_time_plots(target_id, data_sets) {
    show_empty_plot(target_id, 'loading...');

    $.getJSON($SCRIPT_ROOT + '/api/time_plots', data_sets, function(viz) {
        convert_data_array(viz);

        viz.full_width = true;
        viz.height = 500;
        viz.right = 80;
        viz.target = target_id;

        MG.data_graphic(viz);
    }).fail(function() {
        show_empty_plot(target_id, 'sorry, an error occurred');
    });
};

function updateLiveUpdate(params) {
        if(params['time_delta'] !== undefined) {
          live_params['time_delta'] = params['time_delta'];
        }

        if(params['max_size'] !== undefined) {
          live_params['max_size'] = params['max_size'];
        }
};

function stopLiveUpdate() {
        clearInterval(intervalId);
}

function live_plot(target_id, params) {
        show_empty_plot(target_id, 'loading');

        var route = $SCRIPT_ROOT + '/api/live_plot/' + params.id;
        $.getJSON(route, function(viz) {
        convert_data_array(viz);

        viz.full_width = true;
        viz.height = 400;
        viz.right = 80;
        viz.target = target_id;
        viz.legend_target = '.legend';
        viz.transition_on_update = false;
        live_viz = viz;
        MG.data_graphic(viz);
        live_params = {'max_size': -10, 'time_delta': 30 /* seconds */}
        activateLiveUpdate(route, live_viz, 1000);
    }).fail(function() {
        show_empty_plot(target_id, 'sorry, an error occurred');
    });
};

function startLiveUpdate(data_id) {
        var route = $SCRIPT_ROOT + '/api/live_plot/' + data_id;
        activateLiveUpdate(route, live_viz, 1000);
}

function activateLiveUpdate(route, viz, interval) {
        intervalId = setInterval(function() {
        data = viz['data'][0];
        last_date = data[data.length-1]['date'];
        var get_params = {'last_received': date_to_unix_time_stamp(last_date)};

        $.getJSON(route, get_params, function(new_data) {
            new_data.map(function(d) {
                d['date'] = unix_time_stamp_to_date(d['date']);
                return d;
            });

            if (typeof live_params !== 'undefined' && live_params !== null) {
                if (live_params['max_size'] && live_params['max_size'] > 0) {
                    while (viz['data'][0].length + new_data.length > live_params['max_size']) {
                        viz['data'][0].shift();
                    }
                }
                if (live_params['time_delta'] && live_params['time_delta'] > 0) {
                    var start_timestamp = new Date();
                    start_timestamp.setSeconds(start_timestamp.getSeconds() - live_params['time_delta']);
                    while (viz['data'][0][0]['date'] < start_timestamp) {
                        viz['data'][0].shift();
                    }
                }
            }
            viz['data'][0].push.apply(viz['data'][0], new_data);
            MG.data_graphic(viz);
        }).fail(function() {
            show_empty_plot(target_id, 'sorry, an error occurred');
        });
    }, interval);
};

function acf_plot(target_id, params) {
    show_empty_plot(target_id, 'loading');

    $.getJSON($SCRIPT_ROOT + '/api/acf_plot/' + params.id, params, function(viz) {
        viz.full_width = true;
        viz.height = 400;
        viz.target = target_id;
        viz.legend_target = '.legend';
        viz.y_mouseover = '+.2r';

        MG.data_graphic(viz);
    }).fail(function() {
        show_empty_plot(target_id, 'sorry, an error occurred');
    });
};

function forcasting_eval_plot(target_id, params) {
    show_empty_plot(target_id, 'loading');

    $.getJSON($SCRIPT_ROOT + '/api/forecasting_plot/' + params.id, function(viz) {
        convert_data_array(viz);

        viz.markers.map(function(d) {
            d['date'] = unix_time_stamp_to_date(d['date']);
            return d;
        });

        viz.full_width = true;
        viz.height = 400;
        viz.target = target_id;
        viz.legend_target = '.legend';

        MG.data_graphic(viz);
    }).fail(function() {
        show_empty_plot(target_id, 'sorry, an error occurred');
    });
}

function show_empty_plot(target_id, message) {
    MG.data_graphic({
        chart_type: 'missing-data',
        missing_text: message,
        target: target_id,
        full_width: true,
        height: 400
    });
}

function convert_data_array(viz) {
    for (var i = 0; i < viz.data.length; i++) {
        viz.data[i].map(function(d) {
            d['date'] = unix_time_stamp_to_date(d['date']);
            return d;
        });
    }
}
