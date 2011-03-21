$(document).ready(function() {
    if(!("WebSocket" in window)) {
      alert("Sorry, the build of your browser does not support WebSockets. Please use latest Chrome or Webkit nightly");
      return;
    }

    switch($('meta[name=subpage]').attr('content'))
      {
      case 'top':
        init_top();
        break;
      default:
      }

    window.setInterval(check_status, 1000);
  });

function init_top() {
  ws = new WebSocket("ws://rabbitmq.yourdomain:8080/");
  
  ws.onopen = function() {
    clear_rows();
    ws.send(JSON.stringify({'pool': 'default'}));
  };

  ws.onmessage = function(evt) {
    var json = JSON.parse(evt.data);
    update_row(json);
  };
}

function change_pool() {
  var pool = $('#selected_pool').val();
  clear_rows();
  ws.send(JSON.stringify({'pool': pool}));
}

function clear_rows() {
  $('#pool_data table tbody').html('');
}

function update_row(data) {
  var row = $('#row_' + data['hostname']);
  if (row.length == 0) {
    generate_row(data);
    return;
  }

  var load = row.children('td[content=load]');
  var apache = row.children('td[content=apache]');
  var memory = row.children('td[content=memory]');
  var flags = row.children('td[content=flags]');

  load.html(generate_load(data['load']));
  memory.html(generate_memory(data['memory']));  
  apache.html(generate_apache(data['apache']));
  update_flags(flags, data['flags']);
}

function generate_row(data) {
  var html = '\
<tr id="row_{{hostname}}" pool="{{pool}}">\
  <td class="hostname" content="flags" value={{last_time}}{{#flags}} load="{{load}}" memory="{{memory}}" apache="{{apache}}" timeout="{{timeout}}"{{/flags}}\>\
  </td>\
  <td class="hostname" content="hostname">{{hostname}}</td>\
  <td class="hostname" content="load">' + generate_load(data['load']) + '</td> \
  <td class="hostname" content="memory">' + generate_memory(data['memory']) + '</td>\
  <td class="hostname" content="apache">' + generate_apache(data['apache']) + '</td>\
</tr>\
';
  $('#pool_data table tbody').append(Mustache.to_html(html, data));
}

function generate_load(load) {
  return Mustache.to_html('{{5min}} / {{10min}} / {{15min}}', load);
}

function generate_memory(memory) {
  memory['percent_free'] = memory['percent_free'].toFixed(2);
  return Mustache.to_html('{{percent_free}} / {{free}} / {{total}}', memory);
}

function generate_apache(apache) {
  apache['reqs'] = apache['reqs'].toFixed(2);
  return Mustache.to_html('{{act}} / {{idle}} / {{reqs}}', apache);
}

function update_flags(row, flags) {
  row.attr("load", flags["load"]);
  row.attr("memory", flags["memory"]);
  row.attr("apache", flags["apache"]);
  row.attr("timeout", flags["timeout"]);
}

/* Status */
function check_status() {
  $('#pool_data table tbody tr').each(function() {
      check_time($(this));
    });
}

function check_time(row) {
  
}