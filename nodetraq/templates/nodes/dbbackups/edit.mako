<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript">
  function removeDbBackup(id) {
      if (confirm("Are you sure you want to remove this database backup?")) {
          location = "${h.url(controller='dbbackups', action='destroy', id=c.node_id, backup_id=c.backup_id)}";
      }
  }

  function submit_dbbackup() {
    var enabled = false;
    var is_enabled = $("#enabled:checked");

    if (is_enabled.length > 0)
      enabled = true;
    
    var record_info = {
      'directory': $("#directory").val(),
      'storage': $("#storage").val(),
      'enabled': enabled,
      'backup_type': $("#backup_type").val()
    }

    $.ajax({
      url: "${h.url(controller='dbbackups', action='update', id=c.node_id, backup_id=c.backup_id)}",
      type: 'POST',
      data: JSON.stringify(record_info),
      success: function(response) {
          location = "${h.url(controller='dbbackups', action='index', id=c.node_id)}";
      }
    });
  }
</script>
</%def>


<div id="split_content_right" class="box center">
    <a href="${h.url(controller='dbbackups', action='index', id=c.node_id)}">Show Db backups</a>
</div>

<div style="float: right; margin-right: 2em;" class="box remove_item center">
  <a href="#" onClick="removeDbBackup(${c.node_backup.id});">Remove this backup</a>
</div>

${h.form(url(controller='dbbackups', action='update', id=c.node_id, backup_id=c.backup_id), method='POST')}
Storage: ${h.text('storage', value=c.node_backup.storage.hostname)} <br />
Directory: ${h.text('directory', value=c.node_backup.directory)} <br />
Type: ${h.select('backup_type', 0, c.backup_type_list) } <br />
Enabled: ${h.checkbox('enabled', value=c.node_backup.enabled, checked=c.node_backup.enabled)} <br /> <br />
<input type="button" onClick="submit_dbbackup()" value="Submit"></input>

${h.end_form()}

