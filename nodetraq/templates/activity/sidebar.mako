% if c.subpage == 'info':
<h3>Activity</h3>
% else:
${h.form(url(controller='activity', action='index'), method='get')}
<h3>Activity</h3>
<p>
${h.checkbox('show_nodes', checked=c.filters['show_nodes'])}
<a href="${h.url(controller='activity', action='index', show_nodes=1)}">Nodes</a><br />
${h.checkbox('show_groups', checked=c.filters['show_groups'])}
<a href="${h.url(controller='activity', action='index', show_groups=1)}">Groups</a><br />
${h.checkbox('show_inventory', checked=c.filters['show_inventory'])}
<a href="${h.url(controller='activity', action='index', show_inventory=1)}">Inventory</a><br />
</p>
<p>
<input type="submit" value="Apply">
</p>
${h.end_form()}
% endif

