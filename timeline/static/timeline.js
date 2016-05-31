var time_plot = function(event) {
    var get_params = {
        'start_date': DateToUnixTimeStamp(new Date('2005/06/20 00:00:00')),
        'end_date': DateToUnixTimeStamp(new Date('2005/06/27 23:59:59')),
        'rolling_mean_window': 600,
        'rolling_std_window': 600
    };

    $.getJSON($SCRIPT_ROOT + '/time_plot/0', get_params, function(viz) {
        convertDataArray(viz);

        viz.width = 800;
        viz.height = 400;
        viz.target = $('#time-plot-canvas')[0];

        MG.data_graphic(viz);
    });
};

var multiple_time_plots = function(event) {
    var get_params = {
        'ts1': 'random',
        'ts2': 'random',
        'ts3': 'random'
    };

    $.getJSON($SCRIPT_ROOT + '/time_plots', get_params, function(viz) {
        convertDataArray(viz);

        viz.width = 800;
        viz.height = 400;
        viz.target = $('#multiple-time-plots-canvas')[0];

        MG.data_graphic(viz);
    });
};

var acf_plot = function(event) {
    var get_params = {
        'max_lag': 300
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
