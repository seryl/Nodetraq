<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript" src="/js/users.js"></script>
<meta content="${c.sort_type}" name="sort_type" />
<meta content="${c.sort_order}" name="sort_order" />
</%def>

<%include file="/users/search_form.mako" />

<div style="margin: 0 auto; padding: 0 140px;">
<table class="list">
  <thead>
    <tr>
      <th id="type_header">Type</th>
      <th id="name_header">
        % if c.sort_type == 'cn':
        <a href="${h.url(controller='users', action='groups', order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='cn')}">Name</a>
        % else:
        <a href="${h.url(controller='users', action='groups', order=c.sort_order == 'asc' and 'asc' or 'desc', sort='cn')}">Name</a>
        % endif
      </th>
      <th id="description_header">
        % if c.sort_type == 'description':
        <a href="${h.url(controller='users', action='groups', order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='description')}">Description</a>
        % else:
        <a href="${h.url(controller='users', action='groups', order=c.sort_order == 'asc' and 'asc' or 'desc', sort='description')}">Description</a>
        % endif
      </th>
    </tr>
  </thead>
  <tbody>
    % for i, group in enumerate(c.groups):
    <tr class="${i%2 and 'even' or 'odd'}">
      <td class="is_group"></td>
      % if group[1].has_key('cn'):
      <td class="name">
        <a href="${h.url(controller='users', action='group_members', group=group[1]['cn'][0])}">${group[1]['cn'][0]}</a>
      </td>
      % else:
      <td class="name">
        <a href="${h.url(controller='users', action='group_members', account=group[1])}">${group[1]}</a>
      </td>
      % endif
      % if group[1].has_key('description'):
      <td class="email">${group[1]['description'][0]}</td>
      % else:
      <td class="email"></td>
      % endif
    </tr>
    % endfor
  </tbody>
</table>
</div>
