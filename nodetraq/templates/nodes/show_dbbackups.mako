<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript" src="/js/dbbackups.js"></script>
</%def>

% if c.active_user['user_level'] == 0:
<div id="split_content_right" class="box center" style="margin-bottom: 10px;">
  <a href="${h.url(controller='nodes', action='edit_bulk_dbbackups')}">Edit</a>
</div>
<br />
% endif

<div style="width: 600px; margin: 0 auto;">

<table class="list">
  <thead>
    <tr>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='server')}">Server</a></th>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='storage')}">Storage</th>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='directory')}">Directory</th>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='backup_type')}">Type</th>
      <th><a href="${h.url(controller='nodes', action='show_dbbackups', sort='enabled')}">Enabled</th>
    </tr>
  </thead>
  <tbody>
    % for i, backup in enumerate(c.dbbackups):
    <tr class="${i%2 and 'even' or 'odd'}" node="${backup.server_id}", backup_id="${backup.id}">
      <td class="hostname">
        <a href="${h.url(controller='dbbackups', action='index', id=backup.server_id)}">${backup.server.hostname}</a>
      </td>
      <td class="hostname">
        <a href="${h.url(controller='dbbackups', action='edit', id=backup.server_id, backup_id=backup.id)}">${backup.storage.hostname}</a>
      </td>
      <td class="hostname">
        <a href="${h.url(controller='dbbackups', action='edit', id=backup.server_id, backup_id=backup.id)}">${backup.directory}</a>
      </td>
      <td class="hostname">
        <a href="${h.url(controller='dbbackups', action='edit', id=backup.server_id, backup_id=backup.id)}">${backup.backup_type.name}</a>
      </td>
      <td class="toggleable ${backup.enabled and 'enabled' or 'disabled'}"></td>
    </tr>
    % endfor
  </tbody>
</table>

</div>
