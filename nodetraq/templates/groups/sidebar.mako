<h3>Groups</h3>

<ul class="no-dec">

% if not c.subpage == 'list':
<li>
    <a href="${h.url(controller='groups', action='index')}">List groups</a>
</li>
% endif

% if not c.subpage == 'new':
<li>
    <a href="${h.url(controller='groups', action='new')}">Create group</a>
</li>
% endif

% if not c.subpage == 'modify':
<!--
<li>
    <a href="${h.url(controller='groups', action='modify')}">Modify groups</a>
</li>
-->
% endif

</ul>
% if c.all_groups:
<h3>Cloud</h3>
<p class="tag_cloud">
<% group_len = len(c.all_groups) %>
% for i, group in enumerate(c.all_groups):
% if group_len-1 == i:
<a href="${h.url(controller='groups', action='show', id=group.id)} style="font-size: ${c.tag_sizes[group.name]}px;">${group}</a>
% else:
<a href="${h.url(controller='groups', action='show', id=group.id)}" style="font-size: ${c.tag_sizes[group.name]}px;">${group}</a>,
% endif
% endfor
</p>
% endif

