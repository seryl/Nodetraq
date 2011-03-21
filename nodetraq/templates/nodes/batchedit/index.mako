<%inherit file="/common/base.mako" />
<%def name="head_tags()">
    <meta content="${c.field}" name="field_type" />
    <meta content="${c.active_user['user_id']}" name="user_id" />
    <script type="text/javascript" src="/js/batchedit.js"></script>
</%def>

<div style="width: 100%; text-align: center; display: block;">
  <h1>Editing: ${c.field}</h1>
</div>

<input type="hidden" name="field" value="${c.field}" />
<div id="batchedit">
  <table width="100%">
    <thead>
      <tr>
        <th>
          Old Values
        </th>
        <th>
          New Values
        </th>
      </tr>
    </thead>
    <tbody>
      %if c.field == 'hostname':
      %for node in c.nodes:
      <tr>
        <th>
          <a href="${h.url(controller='nodes', action='show', id=node.id)}">${node.hostname}<a/>
        </th>
        <th>
          ${node.hostname}
        </th>
      </tr>
      <tr>
        <th>
          ${h.text('hostname_' + str(node.id), getattr(node, c.field), data="old", hostname=node.hostname, node_id=node.id, disabled="true")}
        </th>
        <th>
          ${h.text('new_hostname_' + str(node.id), '', data="new", hostname=node.hostname, node_id=node.id)}
        </th>
      </tr>
      %endfor

      %elif c.field == 'groups':
      %for node in c.nodes:
      <tr>
        <th>
          <a href="${h.url(controller='nodes', action='show', id=node.id)}">${node.hostname}<a/>
        </th>
      </tr>
      <tr>
        <th>
          ${h.text('old_groups', ", ".join([g.name for g in node.groups]), data="old", hostname=node.hostname, node_id=node.id)}
        </th>
        <th>
          ${h.text('new_groups', ", ".join([g.name for g in node.groups]), data="new", hostname=node.hostname, node_id=node.id)}
        </th>
      </tr>
      %endfor

      %elif c.field == 'db_backups':
      %for node in c.nodes:
      <tr>
        <th>
          <a href="${h.url(controller='nodes', action='show', id=node.id)}">${node.hostname}<a/>
        </th>
      </tr>
      %for dbbackup in node.db_backups:
      <tr>
        <th>
          Storage: ${h.text('storage_' + str(dbbackup.id), dbbackup.storage.hostname, data="old", node_id=node.id)}<br />
          Directory: ${h.text('directory_' + str(dbbackup.id), dbbackup.directory, data="old", node_id=node.id)}
        </th>
        <th>
          Storage: ${h.text('new_storage_' + str(dbbackup.id), dbbackup.storage.hostname, data="new", node_id=node.id, data_type="storage", backup_id=dbbackup.id)}<br />
          Directory: ${h.text('new_directory_' + str(dbbackup.id), dbbackup.directory, data="new", node_id=node.id, data_type="directory", backup_id=dbbackup.id)}
        </th>
      </tr>
      %endfor
      %endfor
      %endif
      <tr>
        <th>
        </th>
        <th style="padding-top: 20px;">
          <input id="none" type="submit" value="Submit" onClick="send_batch_request();" />
        </th>
      </tr>
    </tbody>
  </table>
</div>
