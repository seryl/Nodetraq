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
      <th id="account_header">
        % if c.sort_type == 'uid':
        <a href="${h.url(controller='users', action='index', order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='uid')}">Account</a>
        % else:
        <a href="${h.url(controller='users', action='index', order=c.sort_order == 'asc' and 'asc' or 'desc', sort='uid')}">Account</a>
        % endif
      </th>
      <th id="name_header">
        % if c.sort_type == 'cn':
        <a href="${h.url(controller='users', action='index', order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='cn')}">Name</a>
        % else:
        <a href="${h.url(controller='users', action='index', order=c.sort_order == 'asc' and 'asc' or 'desc', sort='cn')}">Name</a>
        % endif
      </th>
      <th id="email_header">
        % if c.sort_type == 'mail':
        <a href="${h.url(controller='users', action='index', order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='mail')}">Email</a>
        % else:
        <a href="${h.url(controller='users', action='index', order=c.sort_order == 'asc' and 'asc' or 'desc', sort='mail')}">Email</a>
        % endif
      </th>
      <th id="enabled_header">
        % if c.sort_type == 'nsAccountLock':
        <a href="${h.url(controller='users', action='index', order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='nsAccountLock')}">Enabled</a>
        % else:
        <a href="${h.url(controller='users', action='index', order=c.sort_order == 'asc' and 'asc' or 'desc', sort='nsAccountLock')}">Enabled</a>
        % endif
      </th>
    </tr>
  </thead>
  <tbody>
    % for i, user in enumerate(c.users):
    <tr class="${i%2 and 'even' or 'odd'}">
      % if user[1].has_key('ou'):
      <td class="is_user">${user[1]['ou']}</td>
      % else:
      <td class="is_user"></td>
      % endif
      % if user[1].has_key('sAMAccountName'):
      <td class="account">
        <a href="${h.url(controller='users', action='edit', account=user[1]['sAMAccountName'][0])}">${user[1]['sAMAccountName'][0]}</a>
      </td>
      % else:
      <td class="account">
        <a href="${h.url(controller='users', action='edit', account=user[1]['uid'][0])}">${user[1]['uid'][0]}</a>
      </td>
      % endif
      % if user[1].has_key('name'):
      <td class="name">${user[1]['name'][0]}</td>
      % elif user[1].has_key('cn'):
      <td class="name">${user[1]['cn'][0]}</td>
      % else:
      <td class="name"></td>
      % endif
      % if user[1].has_key('mail'):
      <td class="email">${user[1]['mail'][0]}</td>
      % else:
      <td class="email"></td>
      % endif
      % if user[1].has_key('nsAccountLock'):
      <td class="${user[1]['nsAccountLock'][0].lower() == 'false' and 'enabled' or 'disabled'}"></td>
      % else:
      <td class="enabled"></td>
      % endif
    </tr>
    % endfor
  </tbody>
</table>
</div>
