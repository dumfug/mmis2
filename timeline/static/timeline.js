var time_plot = function(event) {
    var get_params = {
        'start_date': DateToUnixTimeStamp(new Date('2005/06/20 00:00:00')),
        'end_date': DateToUnixTimeStamp(new Date('2005/06/27 23:59:59')),
        'rolling_mean_window': 600,
        'rolling_std_window': 600
    }

    $.getJSON($SCRIPT_ROOT + '/time_plot/0', get_params, function(viz) {
        // convert unix timestamp into JS date object
        for (var i = 0; i < viz.data.length; i++) {
            viz.data[i].map(function(d) {
                d['date'] = UnixTimeStampToDate(d['date']);
                return d;
            });
        }

        viz.width = 800;
        viz.height = 400;
        viz.target = $('#time-plot-canvas')[0];

        MG.data_graphic(viz);
    });
};

function DateToUnixTimeStamp(date) {
    return Math.round(date.getTime() / 1000);
}

function UnixTimeStampToDate(time_stamp) {
    return new Date(time_stamp * 1000);
}
