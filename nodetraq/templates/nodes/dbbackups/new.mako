<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>


<div id="split_content_right" class="box center">
    <a href="${h.url(controller='dbbackups', action='index', id=c.node_id)}">Show Db backups</a>
</div>

${h.form(url(controller='dbbackups', action='create', id=c.node_id), method='POST')}
Storage: ${h.text('storage')} <br />
Directory: ${h.text('directory')} <br />
Type: ${h.select('backup_type', 0, c.backup_type_list) } <br /> <br />
${h.submit(None, 'Submit')}
${h.end_form()}

