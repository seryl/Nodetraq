<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%def name="head_tags()">
</%def>

<h2>Load balancer</h2>

<table class="list">
<thead>
    <tr>
    <th><a href="">Pool</a></th>
    <th><a href="">Members</a></th>
    </tr>
</thead>
<tbody>
% for i, pool in enumerate(c.members):
    <tr class="${i%2 and 'even' or 'odd'}">
    <td class="group"><a href="${url(controller='loadbalancer', action='show', pool=pool[0])}">${pool[0]}</a></td>
    <td>
    % for x,node in enumerate(pool[1]):
        % if node[0]:
    <a href="${url(controller='nodes', action='show', id=node[0].id)}">${node[0].hostname}</a>,
        % endif
    % endfor
    </td>
% endfor
</tbody>
</table>

<p class="pagination">
<%call expr="generate_pagination(c.page, c.total_pages, c.current_page_count, c.pool_count, c.link_append)"></%call>
</p>
