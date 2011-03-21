<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link rel="stylesheet" type="text/css" href="/css/users.css" />
<script type="text/javascript" src="/js/users.js"></script>
<meta content="${c.sort_type}" name="sort_type" />
<meta content="${c.sort_order}" name="sort_order" />
<meta content="${c.group}" name="group" />
<script type="text/javascript">
  $('.list input[type="checkbox"]:checked').each(function() {
  ($(this).parent().parent().addClass('context-menu-selection'));
  });
</script>
</%def>

<h2 style="float: left;">${c.group}</h2>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='users', action='editgroup', group=c.group)}">Edit this group</a>
</div>

${h.form(url(controller="users", action="update_group_users"),'POST', group=c.group, name='group_form')}
<div id="group_form">
  <table width="100%">
    <thead>
    </thead>
    <tbody>
      <tr>
        <td>
          <p class="buttons">
            <a class="icon icon-checked" onclick="apply_group_function();" href="#">Apply</a>
            <a class="icon icon-reload" onclick="clear_checked();" href="#">Clear</a>
          <span style="float: right;">
          ${h.select('function', 0, [
              ('remove_group_member', 'Remove from group'),
          ])}
          </span>
          </p>
        </td>
      </tr>
    </tbody>
  </table>
</div>
${h.end_form()}

<div style="margin: 0 auto; padding: 0 140px;" />
<table class="list">
  <thead>
    <tr>
      <th><a class="check_toggle" href="javascript:toggle_checked()"><img src="/images/toggle_check.png" alt="Toggle_check"></a> </th>
      <th id="account_header">
        % if c.sort_type == 'uid':
        <a href="${h.url(controller='users', action='group_members', group=c.group, order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='uid')}">Account</a>
        % else:
        <a href="${h.url(controller='users', action='group_members', group=c.group, order=c.sort_order == 'asc' and 'asc' or 'desc', sort='uid')}">Account</a>
        % endif
      </th>
      <th id="name_header">
        % if c.sort_type == 'cn':
        <a href="${h.url(controller='users', action='group_members', group=c.group, order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='cn')}">Name</a>
        % else:
        <a href="${h.url(controller='users', action='group_members', group=c.group, order=c.sort_order == 'asc' and 'asc' or 'desc', sort='cn')}">Name</a>
        % endif
      </th>
      <th id="email_header">
        % if c.sort_type == 'mail':
        <a href="${h.url(controller='users', action='group_members', group=c.group, order=not c.sort_order == 'asc' and 'asc' or 'desc', sort='mail')}">Email</a>
        % else:
        <a href="${h.url(controller='users', action='group_members', group=c.group, order=c.sort_order == 'asc' and 'asc' or 'desc', sort='mail')}">Email</a>
        % endif
      </th>
    </tr>
  </thead>
  <tbody>
    % for i, user in enumerate(c.members):
    <tr class="${i%2 and 'even' or 'odd'}">
      <td class="checkbox">
        % if user[1].has_key('sAMAccountName'):
        <input class="ShiftCheckbox" type="checkbox" name="${user[1]['sAMAccountName'][0]}" value="${user[1]['sAMAccountName'][0]}">
        % else:
        <input class="ShiftCheckbox" type="checkbox" name="${user[1]['uid'][0]}" value="${user[1]['uid'][0]}">
        % endif
      </td>
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
    </tr>
    % endfor
  </tbody>
</table>
</div>
