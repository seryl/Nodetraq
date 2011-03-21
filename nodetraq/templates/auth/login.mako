<%inherit file="/auth/base.mako" />

<div id="login_form" class="box">
    ${h.form(h.url(controller='auth', action='login'), method='post')}

    <table>
      <thead>
        <tr>
          <th colspan=2>Login</th>
        <tr>
      </thead>
      <tbody>
        <tr>
          <td>Username: </td>
          <td>${h.text('username')}</td>
        </tr>
        <tr>
          <td>Password: </td>
          <td>${h.password('password')}</td>
        </tr>
        <tr>
          <td style="text-align: right; padding-top: 10px;" colspan=2>
            ${h.submit('login_submit', 'Login')}</td>
        </tr>
      </tbody>
    </table>

    ${h.end_form()}
</div>
