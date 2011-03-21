<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript">
  function bulk_update() {
    // Get Updates
    var update_list = { "updates": new Array(), "new_backups": new Array() };
    $("tr[dbbackup_id]").each( function(i, row) {
      if ($(row).attr("dbbackup_id") != "new") {
        var update_item = new Object();
        update_item.id = $(row).attr("dbbackup_id");
        update_item.server = $(row).children("td[attrib=server]").children("input").val();
        update_item.storage = $(row).children("td[attrib=storage]").children("input").val();
        update_item.directory = $(row).children("td[attrib=directory]").children("input").val();
        update_item.enabled = false;
        $(row).children("td[attrib=enabled]").children("input[type='checkbox']:checked").each(
          function() {
            update_item.enabled = true;
          });
        update_list["updates"].push(update_item);
      }
    });

    // Get New Ones
    $("tr[dbbackup_id=new]").each( function(i, row) {
      var new_item = new Object();
      new_item.server = $(row).children("td[attrib=server]").children("input").val();
      new_item.storage = $(row).children("td[attrib=storage]").children("input").val();
      new_item.directory = $(row).children("td[attrib=directory]").children("input").val();
      new_item.enabled = false;
      $(row).children("td[attrib=enabled]").children("input[type='checkbox']:checked").each(
        function() {
          new_item.enabled = true;
        });
      update_list["new_backups"].push(new_item);
    });

    $.ajax({
      type: 'POST',
      url: '/dbbackups/bulk_update',
      data: JSON.stringify(update_list),
      success: function(data) {
        console.log(data);
        window.location.reload();
      }
    });
  }

  function add_backup() {
    var last = $("tr[dbbackup_id]:last");
    var count = parseInt($("tr[dbbackup_id]:last").attr("count"));
    if (count) {
      count += 1;
    } else {
      count = 1;
    }
    if (last.hasClass("even")) {
      var nextClass = "odd";
    } else {
      var nextClass = "even";
    }
    $("<tr class=\"" + nextClass + "\" dbbackup_id=\"new\" id=\"new_backup_" + count + "\" count=\"" + count + "\">\n" + \
      "    <td class=\"hostname\" attrib=\"remove\">\n" + \
      "        <a href=\"javascript:remove_backup(new_backup_" + count + ");\">" + "Remove" + "</a>" + \
      "    </td>\n" + \
      "    <td class=\"hostname\" attrib=\"server\">\n" + \
      "        <input id=\"server_hostname\" name=\"server_hostname\" type=\"text\" value=\"\">" + \
      "    </td>\n" + \
      "    <td class=\"hostname\" attrib=\"storage\">\n" + \
      "        <input id=\"server_storage\" name=\"server_storage\" type=\"text\" value=\"\">" + \
      "    </td>\n" + \
      "    <td class=\"hostname\" attrib=\"directory\">\n" + \
      "        <input id=\"server_directory\" name=\"server_directory\" type=\"text\" value=\"\">" + \
      "    </td>\n" + \
      "    <td class=\"hostname\" attrib=\"enabled\">\n" + \
      "        <input checked=\"checked\" id=\"enabled\" name=\"enabled\" type=\"checkbox\" value=\"1\">" + \
      "    </td>\n" + \
      "</tr>").insertAfter(last);
  }

  function remove_backup(id) {
    if (confirm("Are you sure you want to remove this backup?")) {
      if ($(id).attr("id").indexOf("new") != 0) {
        $.ajax({
          url: '/dbbackups/delete/' + $(id).attr("dbbackup_id"),
          success: function(data) {
            console.log(data);
          }
        });
      }
      $(id).remove();
    }
  }
</script>
</%def>

<div id="split_content_right">
  <div class="box center">
    <a href="${h.url(controller='nodes', action='show_dbbackups')}">Show</a>
  </div>

  <div class="box center" style="margin-top: 60px;">
    <a href="#" onClick="bulk_update();">Update</a>
  </div>
</div>

<div style="width: 800px; margin: 0 auto;">

<table class="list">
  <thead>
    <tr>
      <th>Remove?</th>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='server')}">Server</a></th>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='storage')}">Storage</th>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='directory')}">Directory</th>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='enabled')}">Enabled</th>
    </tr>
  </thead>
  <tbody>
    % for i, backup in enumerate(c.dbbackups):
    <tr class="${i%2 and 'even' or 'odd'}" dbbackup_id=${backup.id} id="backup_${backup.id}">
      <td class="hostname" attrib="remove">
        <a href="javascript:remove_backup(backup_${backup.id});">Remove</a>
      </td>
      <td class="hostname" attrib="server">
        ${h.text('server_hostname', backup.server.hostname)}
      </td>
      <td class="hostname" attrib="storage">
        ${h.text('storage_hostname', backup.storage.hostname)}
      </td>
      <td class="hostname" attrib="directory">
        ${h.text('directory', backup.directory)}
      </td>
      <td class="hostname" attrib="enabled">
        ${h.checkbox('enabled', checked=backup.enabled)}
      </td>
    </tr>
    % endfor
    <tr class="additional_options" id="add_backup">
      <td colspan=4></td>
      <td class="hostname" style="padding: 10px 0px;">
        <a href="#add_backup" onClick="add_backup();">Add Backup<a/>
      </td>
    </tr>
  </tbody>
</table>

</div>
