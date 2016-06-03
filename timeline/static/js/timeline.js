var time_plot = function(event) {
    var params = event.data;

    $.getJSON($SCRIPT_ROOT + '/time_plot/' + params.id, params, function(viz) {
        convertDataArray(viz);

        viz.full_width = true;
        viz.height = 400;
        viz.target = $(params.target)[0];
        viz.right = 40;

        MG.data_graphic(viz);
    });
};

function multiple_time_plots(target_id, data_sets) {
    $.getJSON($SCRIPT_ROOT + '/time_plots', data_sets, function(viz) {
        convertDataArray(viz);

        viz.full_width = true;
        viz.height = 500;
        viz.right = 80;
        viz.target = target_id;

        MG.data_graphic(viz);
    });
};

var live_plot = function(event) {
        var route = $SCRIPT_ROOT + '/live_plot/random_live';
        $.getJSON(route, function(viz) {
        convertDataArray(viz);

        viz.width = 800;
        viz.height = 400;
        viz.right = 80;
        viz.target = $('#live-plot-canvas')[0];
        viz.legend_target = '.legend';
        viz.transition_on_update = false;

        MG.data_graphic(viz);
        activateLiveUpdate(viz, 1000, {'max_size': -10, 'time_delta': 30 /* seconds */});
    });

    function activateLiveUpdate(viz, interval, window) {
        setInterval(function() {
            var data = viz['data'][0];
            var last_date = data[data.length-1]['date'];
            var get_params = {'last_received': DateToUnixTimeStamp(last_date)};

            $.getJSON(route, get_params, function(new_data) {
                new_data.map(function(d) {
                    d['date'] = UnixTimeStampToDate(d['date']);
                    return d;
                });

                if (typeof window !== 'undefined' && window !== null) {
                    if (window['max_size'] && window['max_size'] > 0) {
                        while (viz['data'][0].length + new_data.length > window['max_size']) {
                            viz['data'][0].shift();
                        }
                    }
                    if (window['time_delta'] && window['time_delta'] > 0) {
                        var start_timestamp = new Date();
                        start_timestamp.setSeconds(start_timestamp.getSeconds() - window['time_delta']);
                        while (viz['data'][0][0]['date'] < start_timestamp) {
                            viz['data'][0].shift();
                        }
                    }
                }

                viz['data'][0].push.apply(viz['data'][0], new_data);
                MG.data_graphic(viz);
            });
        }, interval);
    }
};

var acf_plot = function(event) {
    var get_params = {
        'max_lag': 300,
        'scale': true
    };

    $.getJSON($SCRIPT_ROOT + '/acf_plot/0', get_params, function(viz) {
        viz.width = 800;
        viz.height = 400;
        viz.target = $('#acf-plot-canvas')[0];
        viz.legend_target = '.legend';
        viz.y_mouseover = '+.2r';

        MG.data_graphic(viz);
    });
};

var forcasting_eval_plot = function(event) {
    $.getJSON($SCRIPT_ROOT + '/forecasting_plot/0', function(viz) {
        convertDataArray(viz);

        viz.markers.map(function(d) {
            d['date'] = UnixTimeStampToDate(d['date']);
            return d;
        });

        viz.width = 800;
        viz.height = 400;
        viz.target = $('#forecasting-plot-canvas')[0];
        viz.legend_target = '.legend';

        MG.data_graphic(viz);
    });
}

function create_empty_plot(target_id, message) {
    MG.data_graphic({
        chart_type: 'missing-data',
        missing_text: message,
        target: target_id,
        full_width: true,
        height: 400
    });
}

function convertDataArray(viz) {
    for (var i = 0; i < viz.data.length; i++) {
        viz.data[i].map(function(d) {
            d['date'] = UnixTimeStampToDate(d['date']);
            return d;
        });
    }
}

function DateToUnixTimeStamp(date) {
    return Math.round(date.getTime() / 1000);
}

function UnixTimeStampToDate(time_stamp) {
    return new Date(time_stamp * 1000);
}
