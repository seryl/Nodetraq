<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<h2>Games</h2>

<table class="list">
<thead>
  <tr>
    <th><a href="">Name</a></th>
    <th><a href="">Description</a></th>
    <th><a href="">Edit</a></th>
  </tr>
</thead>
<tbody>
  % for game in c.games:
  <tr>
    <td class="hostname">${h.link_to(game.name, h.url(controller='nodes', action='show_game', id=game.id))}</td>
    <td class="hostname">${game.description}</td>
    <td class="hostname">${h.link_to('Edit', h.url(controller='nodes', action='edit_game', id=game.id))}</td>
  </tr>
  % endfor
</tbody>
</table>

