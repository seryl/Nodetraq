<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='show', id=c.node_id)}">Back</a> <br />
    <a href="${h.url(controller='vhosts', action='new', id=c.node_id)}">New vhost</a>
</div>

<h2>${c.header}</h2>

% for vhost in c.node.vhosts:
    Hostname: <a href="${h.url(controller='vhosts', action='edit', id=c.node.id, vhostid=vhost.id)}">${vhost.hostname}</a><br />
    Comment: ${vhost.comment} <br /><br />
% endfor

