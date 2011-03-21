<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<h2>Studios</h2>

<table class="list">
<thead>
  <tr>
    <th><a href="">Name</a></th>
    <th><a href="">Description</a></th>
    <th><a href="">Edit</a></th>
  </tr>
</thead>
<tbody>
  % for studio in c.studios:
  <tr>
    <td class="hostname">${h.link_to(studio.name, h.url(controller='nodes', action='show_studio', id=studio.id))}</td>
    <td class="hostname">${studio.description}</td>
    <td class="hostname">${h.link_to('Edit', h.url(controller='nodes', action='edit_studio', id=studio.id))}</td>
  </tr>
  % endfor
</tbody>
</table>

