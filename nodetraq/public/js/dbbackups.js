$(document).ready(function() {
    $('.toggleable').live('click', toggle_enabled);
});

function toggle_enabled() {
  var column = $(this);
  var row = column.parent();
  var is_enabled = column.hasClass('enabled');
  if (is_enabled) {
    var action = 'disable';
  } else {
    var action = 'enable';
  }

  var data = {
    'node': row.attr("node"),
    'backup_id': row.attr("backup_id"),
    'action': action
  };

  var url = '/nodes/{{node}}/dbbackups/{{backup_id}}/{{action}}';
  
  $.ajax({
      url: Mustache.to_html(url, data),
      type: 'POST',
      success: function(response) {
        if (response["success"] == true) {
          update_column(column, !is_enabled);
        }
      }
    });
}

function update_column(col, enabled) {
  if (enabled) {
    col.removeClass('disabled');
    col.addClass('enabled');
  } else {
    col.removeClass('enabled');
    col.addClass('disabled');
  }
}