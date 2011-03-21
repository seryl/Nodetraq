${h.form(url(controller='users', action='rename_user_service', account=c.account), method='post')}
<div style="align: center; font-weight: bold;">Rename user</div>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>Current:</td>
      <td>${h.text('current_username', value=c.account, disabled=True)}</td>
    </tr>
    <tr>
      <td>New:</td>
      <td>${h.text('new_username')}</td>
    </tr>
    <tr>
      <td colspan="2" class="align-right">${h.submit(None, 'Submit')}</td>
    </tr>
  </tbody>
</table>

${h.end_form()}
