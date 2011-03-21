% if not c.search_type or c.search_type == 'users':
${h.form(url(controller='users', action='index'), id="search_form")}
% else:
${h.form(url(controller='users', action='groups'), id="search_form")}
% endif


<div id="search_div" style="margin: 0 auto; padding: 0 140px;">
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>Search</td>
      <td><div class="form_input">${h.text("search_field")}</div></td>
      <td style="float: right;">
        ${h.submit(None, 'Search')}
      </td>
      <td onClick="update_search();">
        % if not c.search_type or c.search_type == 'users':
        ${h.radio('search_type', 'users', True, 'Users')}
        ${h.radio('search_type', 'groups', False, 'Groups')}
        % else:
        ${h.radio('search_type', 'users', False, 'Users')}
        ${h.radio('search_type', 'groups', True, 'Groups')}
        % endif
      </td>
    </tr>
  </tbody>
</table>
</div>

${h.end_form()}
