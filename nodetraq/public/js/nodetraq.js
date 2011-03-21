$(document).ready(function() {
    // Set the selected page
    var page = $("meta[name='selected_page']").attr('content');
    if (page) {
        $("."+page).addClass("selected");
    }

    // Show flash status
    if (!$("#flash").hasClass('hidden')) {
        hideFlash();
    }
});

(function($) {
    $.mustache = function(template, view, partials) {
        return Mustache.to_html(template, view, partials);
    };
})(jQuery);

$( function() {
        $('.list .checkbox input:checkbox').click(update_context_selector);
        if ($('.list .checkbox').length != 0) {
            $('.ShiftCheckbox').shiftcheckbox();
        }
});

/* Generate fragment of random numbers */
jQuery._uuid_default_prefix = '';
jQuery._uuidlet = function () {
  return (((1+Math.random())*0x10000|0).toString(16).substring(1));
};

/* Generates random uuid */
jQuery.uuid = function (p) {
	if (typeof(p) == 'object' && typeof(p.prefix) == 'string') {
		jQuery._uuid_default_prefix = p.prefix;
	} else {
		p = p || jQuery._uuid_default_prefix || '';
		return(p+jQuery._uuidlet()+jQuery._uuidlet()+"-"+jQuery._uuidlet()+"-"+jQuery._uuidlet()+"-"+jQuery._uuidlet()+"-"+jQuery._uuidlet()+jQuery._uuidlet()+jQuery._uuidlet());
	};
};

function toggle_checked() {
    var c_status = $("meta[name='check_status']").attr('content');
    var new_status = (c_status=='false') ? true : false;
    $("meta[name='check_status']").attr('content', new_status);
    var node_list = $('.list .checkbox input:checkbox');
    node_list.attr('checked', new_status);
    var row = node_list.parent().parent();

    if (new_status == true) {
        row.addClass('context-menu-selection');
    } else {
        row.removeClass('context-menu-selection');
    }
}

function update_context_selector() {
    var row = $(this).parent().parent();

    if($(this).attr('checked')) {
        row.addClass('context-menu-selection');
    } else {
        row.removeClass('context-menu-selection');
    }
}

function toggleFieldset(field) {
    var parent_field = $(field).parent();

    if (parent_field.hasClass('collapsed')) {
        parent_field.removeClass('collapsed');
        parent_field.children("div").slideDown();
    } else {
        parent_field.addClass('collapsed');
        parent_field.children("div").slideUp();
    }
}

function hideFlash() {
    $("#flash").delay(2000)
        .animate({height: 0, opacity: 0}, 'slow', null,
                function() {
                $("#flash").addClass('hidden');
            });
}

function showFlash() {
    $("#flash").removeClass('hidden');
    hideFlash();
}

function clear_checked() {
    // Remove the checkboxes
    $(".list input[type='checkbox']:checked")
        .each(function () {
            $(this).attr('checked', false);
            $(this).parent().parent()
                .removeClass('context-menu-selection');
        });

    // Remove any extra variables set in the outgoing params
}

function apply_function() {
    if ($('#cb_add_group').attr('checked')) {
        var selected = $("#function").val();
        this['run_'+ selected]();
    } else {
        document.query_form.submit();
    }
}

function run_add_group() {
    var selected = $("#selected_group").val();
    var ids = new Array();

    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nodes/addgroups',
        data: {'groups': selected, 'ids': ids},
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_remove_group() {
    var selected = $("#selected_group").val();
    var ids = new Array();

    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nodes/removegroups',
        data: { 'groups': selected, 'ids': ids },
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_disable_host() {
    var ids = new Array();
    var pool = $("input[name='pool']").val();
    var ports = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
            ports.push($(this).parent()
                  .parent().find(".port").text());
        });

    $.ajax({
        url: '/loadbalancer/disablehost.json',
        data: { 'ids': ids , 'pool': pool, 'ports': ports },
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });

}

function run_enable_host() {
    var ids = new Array();
    var pool = $("input[name='pool']").val();
    var ports = new Array();

    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
            ports.push($(this).parent()
                      .parent().find(".port").text());
            });

    $.ajax({
        url: '/loadbalancer/enablehost.json',
        data: { 'ids': ids, 'pool': pool, 'ports': ports },
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_add_lb() {
    var ids = new Array();
    var pool = $("#selected_group").val();
    var port = $("#lb_port").val();
    var ports = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });
    for (id in ids) {
        ports.push(port);
    }
    $.ajax({
        url: '/loadbalancer/addhost.json',
        data: { 'ids': ids, 'pool': pool, 'ports': ports },
        success: function(data) {
        }
    });
    
    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_remove_lb() {
    var ids = new Array();
    var pool = $("input[name='pool']").val();
    var ports = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
            ports.push($(this).parent()
                      .parent().find(".port").text());
        });

    $.ajax({
        url: '/loadbalancer/removehost.json',
        data: { 'ids': ids, 'pool': pool, 'ports': ports },
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_enable_nagios() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nodes/nagios/enable',
        data: { 'ids': ids },
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_disable_nagios() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nodes/nagios/disable',
        data: { 'ids': ids },
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_enable_puppet() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nodes/puppet/enable',
        data: { 'ids': ids },
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_disable_puppet() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nodes/puppet/disable',
        data: { 'ids': ids },
        success: function(data) {
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_edit_flags() {
    $.ajax({
        url: '/nodes/flags/edit',
        success: function(data) {
                $.modal(data);
        }
    });
}

function run_clear_flags() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name'))); 
        });

    $.ajax({
        url: '/nodes/flags/clear',
        data:  { 'ids': ids },
        success: function(data) {
        }
    });

    // Remove scheduled downtime
    $.ajax({
        url: '/nagios/remove_host_downtime',
        type: 'POST',
        data: JSON.stringify({ 'data' : {
              'ids': ids }
        }),
        success: function(data) {
          console.log(data);
        } 
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function call_update_flags() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
                ids.push(parseInt($(this).attr('name'))); 
            });

    var flags = new Array();
    $("#simplemodal-data input[type='checkbox']:checked")
        .each(function() {
                flags.push($(this).attr('name'));
            });

    var description = $("#simplemodal-data textarea")
        .attr('value');
    var username = $("#simplemodal-data input[name='user']")
        .attr('value');

    if (!description) {
        alert('Description can not be empty');
        return null;
    }

    var d = new Date();
    var month = d.getMonth() + 1;
    var date = d.getDate();
    var hours = d.getHours();
    var minutes = d.getMinutes();
    var ampm = 'am';
    if (month < 10) {
      month = '0' + month;
    }
    if (date < 10) {
      date = '0' + date;
    }
    if (hours < 12) {
      ampm = 'am';
    } else {
      ampm = 'pm';
    }
    if (hours > 12) {
      hours = hours - 12;
    }
    if (hours < 10) {
      hours = '0' + hours;
    }
    if (minutes < 10) {
      minutes = '0' + minutes;
    }
    var start_time = month + '/' + date + '/' + d.getUTCFullYear() + 
      ' ' + hours + ':' + minutes + ' ' + ampm;
    var end_time = '';

    $.ajax({
        url: '/nodes/flags/update',
          data: { 'ids': ids,
            'flags': flags,
            'description': description,
            'user': username },
          success: function(data) {
          $.ajax({
              url: '/nagios/schedule_host_downtime',
              type: 'POST',
              data: JSON.stringify({ 'data' : {
                    'ids': ids,
                    'start_time': start_time,
                    'end_time': end_time,
                    'comment': 'Downtime for: ' + flags.join(', '),
                    'author': username,}
                }),
              success: function(data) {
                console.log(data);
              }
            });
        }
      });

    
    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function run_export_csv() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });

    var href = '/nodes/export_csv?';
    var first = true;
    for (id in ids) {
        if (!first) { href += '&'; }
        href += "ids[]=" + ids[id];
        if (first) { first = false; }
    }
    window.location = href;
}

function run_batch_edit() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
            ids.push(parseInt($(this).attr('name')));
        });

    var href = '/nodes/batchedit?';
    var first = true;
    href += 'field=' + $('#selected_field').val();
    for (id in ids) {
        href += '&';
        href += "ids[]=" + ids[id];
    }
    window.location = href;
}

function run_nagios_options() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
             ids.push(parseInt($(this).attr('name')));
        });
    var sel_func = $('#selected_function').val();
    $.ajax({
            url: '/nagios/' + sel_func,
            type: "GET",
            data: { 'ids': ids },
            success: function(data) {
                if (sel_func == 'schedule_downtime') {
                    $.modal(data);
                    $("#start_time").datetimepicker({
                            ampm: true
                        });
                    $("#end_time").datetimepicker({
                            ampm: true
                                });
                    $("#start_time").blur();
                } else {
                    console.log(data);
                }
            }
        });

    $(this).ajaxStop(function() {
            if (sel_func != 'schedule_downtime') {
                location.reload(true);
            }            
    });
}

function run_update_game() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
             ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/games/batch_update_games',
        type: 'POST',
          data: JSON.stringify({
            'ids': ids,
            'game': $('#game').val()
          }),
        success: function(data) {
            console.log(data);
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function flash_error(message) {
}

function add_filter() {
    var select = $("#add_filter_select");
    var field = select.val();
    $("#tr_" + field).attr('style', '');
    $("#cb_" + field).attr('checked', 'true');
    toggle_filter(field);
    select.val(0);

    $("#add_filter_select option[value="+field+"]")
        .attr('disabled', 'disabled');
}

function remove_filters() {
    if ($('#cb_add_group').attr('checked')) {
        if (!$('#filters').hasClass('collapsed')) {
            toggleFieldset('#filters legend');
        }

        $("#filters input[type='checkbox']").attr('checked', '');
        $('#add_filter_select option').attr('disabled', '');

    } else {
        toggleFieldset($('#options legend'));
        toggleFieldset($('#filters legend'));
    }
}

function toggle_filter(field) {
    //console.log(field);
}

function toggle_operator(field) {
    //console.log('operator toggled: %s');
}

function update_options() {
    var selected_func = $('#function').val();

    if (selected_func == 'add_group' ||
            selected_func == 'remove_group') {
        $.ajax({
            url: '/menus/grouplist',
            data: {},
            type: "POST",
            success: function(data) {
                $('.selected_secondary').html(data);
            }
        });
        $('#options_info').html('');
        $('#options_info').attr('style', 'display: none;');
        $('.selected_secondary').html('<img src="/images/loading.gif" /> Loading...');
    } else if (selected_func == 'enable_host' ||
            selected_func == 'disable_host') {
        $('#options_info').html('');
        $('#options_info').attr('style', '');
        $('.selected_secondary').html('');
    } else if (selected_func == 'add_lb') {
        $.ajax({
            url: '/menus/loadbalancerlist',
            data: {},
            type: "POST",
            success: function(data) {
                $('.selected_secondary').html(data);
            }
        });
        $('#options_info').html('Port: <input type="text" name="port" id="lb_port">');
        $('#options_info').attr('style', '');
        $('.selected_secondary').html('<img src="/images/loading.gif" /> Loading...');
    } else if (selected_func == 'batch_edit') {
        $.ajax({
            url: '/menus/batcheditlist',
            data: {},
            type: "POST",
            success: function(data) {
                $('#options_info').html(data);
            }
        });
    } else if (selected_func == 'nagios_options') {
        $.ajax({
            url: '/menus/nagios',
            data: {},
            type: "POST",
            success: function(data) {
                $('#options_info').html(data);
            }
        });
    } else if (selected_func == 'update_game') {
      $.ajax({
          url: '/menus/games',
          data: {},
          type: "POST",
          success: function(data) {
            $('#options_info').html(data);
          }
        });
    } else {
        $('#options_info').html('');
        $('#options_info').attr('style', '');
        $('.selected_secondary').html('');
    }
}

function call_schedule_downtime() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
             ids.push(parseInt($(this).attr('name')));
        });
    var start_time = $('#start_time').val();
    var end_time = $('#end_time').val();
    var comment = $('#comment').val();
    var author = $('#loggedas a').text();

    $.ajax({
        url: '/nagios/schedule_host_downtime',
        type: 'POST',
            data: JSON.stringify({ 'data' : {
            'ids': ids,
            'start_time': start_time,
            'end_time': end_time,
            'comment': comment,
            'author': author,}
        }),
        success: function(data) {
            console.log(data);
        }
        });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function call_enable_host_svc() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
             ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nagios/enable_host_svc',
        type: 'POST',
        data: { 'ids': ids },
        success: function(data) {
            console.log(data);
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function call_disable_host_svc() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
             ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nagios/disable_host_svc',
        type: 'POST',
        data: { 'ids': ids, },
        success: function(data) {
            console.log(data);
        }
    });

    $(this).ajaxStop(function() {
        location.reload(true);
    });
}

function call_remove_all_monitors() {
    var ids = new Array();
    $(".list input[type='checkbox']:checked")
        .each(function() {
             ids.push(parseInt($(this).attr('name')));
        });

    $.ajax({
        url: '/nagios/remove_all_monitors',
        type: 'POST',
        data: { 'ids': ids, },
        success: function(data) {
            console.log(data);
        }
    });
}

function create_downtime_date(d) {
  function pad(n) {
    return n<10 ? '0'+n : n;
  }

  return d.getUTCFullYear()+'-'
    + pad(d.getUTCMonth()+1)+'-'
    + pad(d.getUTCDate())+'T'
    + pad(d.getUTCHours())+':'
    + pad(d.getUTCMinutes())+':'
    + pad(d.getUTCSeconds())+'Z'
}