var time_plot = function(event) {
    $.getJSON($SCRIPT_ROOT + '/time_plot/0',
        {'rolling_mean_window': 600, 'rolling_std_window': 600},
        function(viz) {
            // convert unix timestamp into JS date object
            for (var i = 0; i < viz.data.length; i++) {
                viz.data[i].map(function(d) {
                    d['date'] = new Date(d['date'] * 1000);
                    return d;
                });
            }

            viz.width = 800;
            viz.height = 400;
            viz.target = $('#time-plot-canvas')[0];

            MG.data_graphic(viz);
        });
};
