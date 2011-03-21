<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='vhosts', action='index', id=c.node_id)}">Show vhosts</a>
</div>

<h2>${c.header}</h2>

${h.form(url(controller='vhosts', action='update', id=c.node_id, vhostid=c.vhostid), method='POST')}
Hostname:<br />
${h.text('hostname', value=c.vhost.hostname)} <br />
Comment:<br />
${h.textarea('comment', rows=10, cols=40, value=c.vhost.comment)} <br /> <br />
${h.submit(None, 'Submit')}
${h.end_form()}

