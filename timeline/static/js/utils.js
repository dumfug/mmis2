function show_error(error_message, target_id) {
    $('#' + target_id).append(
        '<div id="timeline_alert_div" class="alert alert-danger"> \
            <a class="close" data-dismiss="alert">×</a> \
            <b><span>' + error_message + '</span></b> \
        </div>'
    );
    setTimeout(function() { $('#timeline_alert_div').remove(); }, 2500);
}
