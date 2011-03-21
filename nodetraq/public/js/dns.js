function remove_dns_record(record_type, host) {
    var domain = $("meta[name=domain]").attr("value");
    var record_info = {
        'domain': domain,
        'type': record_type,
        'host': host
    }

    var question = "Are you sure you want to remove the record: {'{{type}}': '{{host}}'} from {{domain}}?";
    question = Mustache.to_html(question, record_info);
    if (confirm(question)) {
        $.ajax({
            url: '/dns/remove_record',
            type: 'POST',
            data: JSON.stringify(record_info),
            success: function(response) {
                location = "/dns";
            }
        });
    }
}

function update_record_type() {
    var record = $("#record_type").val();
    var count = 0;

    $.ajax({
        url: "/dns/get_new_record",
        type: 'POST',
        data: JSON.stringify({
            'record_type': record,
            'count': count}),
        success: function(response) {
            var selector = $("tr[datatype=selector]");
            $("td[datatype=result]").parent().remove();
            var addnew = $("tr[datatype=addnew]");
            $(response).insertBefore(addnew);
        }
    });
}

function add_new_result() {
    var record = $("#record_type").val();
    var last_result = $("td[datatype=result]:last");
    var count = 0;
    if (last_result) {
        count = last_result.attr("count");
    }
    count++;

    $.ajax({
        url: "/dns/get_new_record",
        type: 'POST',
        data: JSON.stringify({
            'record_type': record,
            'count': count}),
        success: function(response) {
            var selector = $("tr[datatype=selector]");
            var addnew = $("tr[datatype=addnew]");            
            $(response).insertBefore(addnew);
        }
    });
}

function remove_result(count) {
    var result = $("tr td[datatype=result][count=" + count + "]");
    result.parent().remove();
}

function SubmitRecord() {
    var record_type = $("#record_type").val();
    var record_host = $("meta[name=host]").attr("value");
    if (!record_host) {
        record_host = $("#host").val();
    }

    var results = new Array();
    
    $("td[datatype=result]").each(function() {
        var result = {};
        $(this).children("input").each(function() {
            result[$(this).attr("name")] = $(this).val();
          });
        $(this).children("textarea").each(function() {
            result[$(this).attr("name")] = encodeURIComponent($(this).val());
          });
        results.push(result);
    })

      console.log(JSON.stringify({'results': results}));

    $.ajax({
        url: '/dns/update_record',
        data: JSON.stringify({
            'type': record_type,
            'host': record_host,
            'results': results
        }),
        type: 'POST',
        success: function(response) {
            location = "/dns";
        }
    });
}

function publish_record() {
    var domain = $("meta[name=domain]").attr("value");

    $.ajax({
        url: '/dns/push/' + domain,
        type: 'POST',
        success: function(response) {
            location = "/dns";
        }
    });
}

function pull_production() {
    var domain = $("meta[name=domain]").attr("value");

    $.ajax({
        url: '/dns/pull_production/' + domain,
        type: 'POST',
        success: function(response) {
            location = "/dns";
        }
    });
}

function update_diffs() {
  var domain = $("meta[name=domain]").attr("value");
  var rev = $('#revert_list').val();

  $.ajax({
      url: '/dns/get_document_diff/' + domain + '/' + rev,
      type: 'POST',
      success: function(data) {
        $('#diff_id').html(data);
      }
    });
}

function revert_record() {
  var domain = $("meta[name=domain]").attr("value");
  var rev = $('#revert_list').val();

  $.ajax({
      url: '/dns/push/' + domain + '/' + rev,
      type: 'POST',
      success: function(data) {
      location = "/dns";
    }      
  });
}
