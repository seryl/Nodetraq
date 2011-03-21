<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript" src="/js/dbbackups.js"></script>
</%def>

% if c.active_user['user_level'] == 0: 
<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='show', id=c.node_id)}">Back</a> <br />
    <a href="${h.url(controller='dbbackups', action='new', id=c.node_id)}">New Db backup</a>
</div>
<br />
% endif

<h2>${c.header}</h2>
<div class="break"></div>

<table class="list">
<thead>
  <tr>
    <th><a href="">Server</a></th>
    <th><a href="">Storage</a></th>
    <th><a href="">Directory</a></th>
    <th><a href="">Type</a></th>
    <th><a href="">Enabled</a></th>
    <th><a href="">Edit</a></th>
  </tr>
</thead>
<tbody>
  % for i, backup in enumerate(c.node.db_backups):
  <tr node="${backup.server_id}", backup_id="${backup.id}">
    <td class="hostname"><a href="${h.url(controller='nodes', action='show', id=backup.server.id)}">${backup.server.hostname}</a></td>
    <td class="storage"><a href="${h.url(controller='nodes', action='show', id=backup.storage.id)}">${backup.storage.hostname}</a></td>
    <td class="directory">${backup.directory}</td>
    <td class="hostname">${backup.backup_type.name}</td>
    <td class="toggleable ${backup.enabled and 'enabled' or 'disabled'}"></td>
    <td class="edit_option"><a href="${h.url(controller='dbbackups', action='edit', id=c.node_id, backup_id=backup.id)}">Edit</a></td>
  </tr>
  % endfor
</tbody>
</table>

