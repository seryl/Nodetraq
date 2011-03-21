function send_batch_request() {
    var data = {};
    var field = $('meta[name="field_type"]').attr('content');

    data['user_id'] = $('meta[name="user_id"]').attr('content');
    data['field'] = field;
    data['items'] = new Array();;
    if (field == 'hostname') {
        data = batch_hostname($('input[data="new"]'), data);
    } else if (field == 'groups') {
        data = batch_groups($('input[data="new"]'), data);
    } else {
        data = batch_dbbackups($('input[data="new"]'), data);
    }

    $.ajax({
        url: '/nodes/sendbatchedit',
        type: "POST",
                data: data,
        success: function(data) {
                location = '/nodes';
        }
    });
}

function batch_hostname(inputs, data) {
    inputs.each(function() {
            var new_item = "";
            new_item = '{"node_id": "' + $(this).attr('node_id') + '", ';
            new_item += '"hostname": "' + $(this).val() + '"}';
            data['items'].push(new_item);
        });
    return data;
}

function batch_groups(inputs, data) {
    inputs.each(function() {
            var new_item = "";
            new_item = '{"node_id": "' + $(this).attr('node_id') + '", ';
            new_item += '"groups": "' + $(this).val() + '"}';
            data['items'].push(new_item);
        });
    return data;
}

function batch_dbbackups(inputs, data) {
    inputs.each(function() {
            var new_item = "";
            new_item = '{"data_type": "' + $(this).attr('data_type') + '", ';
            new_item += '"value": "' + $(this).val() + '", ';
            new_item += '"node_id": "' + $(this).attr('node_id') + '", ';
            new_item += '"backup_id": "' + $(this).attr('backup_id') + '"}';
            data['items'].push(new_item);
        });
    return data;
}