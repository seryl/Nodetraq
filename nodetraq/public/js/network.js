function update_parent_class() {
    if ($('input[name="logical"]').is(':checked')) {
        if ($('.attr_parent').hasClass('hidden')) {
            $('.attr_parent').removeClass('hidden');
        }
    } else {
        if (!$('.attr_parent').hasClass('hidden')) {
            $('select[name="parent"]').val(0);
            $('.attr_parent').addClass('hidden');
        }
    }
}

function removeDevice(id) {
    if (confirm("Are you sure you want to remove this device?")) {
        $.ajax({
            url: '/network/destroy/'+id,
            type: 'POST',
            data: {},
            success: function(data) {
                location = "/network";
            }
        })
    }
}

function CreateNetworkDevice() {
    var hostname = $('input[name="_hostname"]').val();
    var management_ip = $('input[name="management_ip"]').val();
    var logical = 0;
    if ($('input[name="logical"]').is(':checked')) {
        logical = 1;
    } else{
        logical = 0;
    }
    var type = $('input[name="type"]').val();
    var mac_address = $('input[name="mac_address"]').val();
    var part_number = $('input[name="part_number"]').val();
    var serial_number = $('input[name="serial_number"]').val();
    var parent = $('select[name="parent"]').val();

    $.ajax({
        url: '/network/create',
        type: 'POST',
        data: JSON.stringify({ 'data' : {
            '_hostname': hostname,
            'management_ip': management_ip,
            'logical': logical,
            'type': type,
            'mac_address': mac_address,
            'part_number': part_number,
            'serial_number': serial_number,
            'parent': parent,}
        }),
        success: function(data) {
            console.log(data);
            window.location = '/network';
        }
    });
}

function UpdateNetworkDevice() {
    var device_id = $('meta[name="device_id"]').attr('content');
    var hostname = $('input[name="_hostname"]').val();
    var management_ip = $('input[name="management_ip"]').val();
    var logical = 0;
    if ($('input[name="logical"]').is(':checked')) {
        logical = 1;
    } else{
        logical = 0;
    }
    var type = $('input[name="type"]').val();
    var mac_address = $('input[name="mac_address"]').val();
    var part_number = $('input[name="part_number"]').val();
    var serial_number = $('input[name="serial_number"]').val();
    var parent = $('select[name="parent"]').val();

    $.ajax({
        url: '/network/update/' + device_id,
        type: 'POST',
        data: JSON.stringify({ 'data' : {
            '_hostname': hostname,
            'management_ip': management_ip,
            'logical': logical,
            'type': type,
            'mac_address': mac_address,
            'part_number': part_number,
            'serial_number': serial_number,
            'parent': parent,}
        }),
        success: function(data) {
            console.log(data);
            window.location = '/network';
        }
    });
}
