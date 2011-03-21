<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='edit_studio', id=c.studio.id)}">Edit</a>
</div>

<h2>${c.studio.name}</h2>

<div>
  % for group in c.groups:
  ${group['name']}: ${len(group['nodes'])}<br />
  % endfor
</div>

% for group in c.groups:
% if group['nodes']:
<h2>${group['name']}</h2>

<table class="list">
<thead>
  <tr>
    <th><a href="">Hostname</a></th>
    <th><a href="">Service Tag</a></th>
    <th><a href="">Server ID</a></th>
    <th><a href="">Primary IP</a></th>
    <th><a href="">Drac IP</a></th>
    <th><a href="">Rack</a></th>
    <th><a href="">Rack U</a></th>
  </tr>
</thead>
<tbody>
  % for node in group['nodes']:
  <tr>
    <td class="hostname">${h.link_to(node.hostname, h.url(controller='nodes', action='show', id=node.id))}</td>
    <td class="service_tag">${node.service_tag}</td>
    <td class="server_id">${node.server_id}</td>
    <td class="primary_ip">${node.primary_ip}</td>
    <td class="drac_ip">${node.drac_ip}</td>
    <td class="rack">${node.rack}</td>
    <td class="rack_u">${node.rack_u}</td>
  </tr>
  % endfor
</tbody>
</table>

% endif
% endfor
