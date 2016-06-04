function show_error(error_message, target_id) {
    $('#' + target_id).append(
        '<div id="timeline_alert_div" class="alert alert-danger"> \
            <a class="close" data-dismiss="alert">×</a> \
            <b><span>' + error_message + '</span></b> \
        </div>'
    );
    setTimeout(function() { $('#timeline_alert_div').remove(); }, 2500);
}

function date_to_unix_time_stamp(date) {
    return Math.round(date.getTime() / 1000);
}

function unix_time_stamp_to_date(time_stamp) {
    return new Date(time_stamp * 1000);
}
