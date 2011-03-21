<html>
  <head></head>
  <body>
% if c.new_account:
Hi ${c.full_name},<br /><br />

Welcome to YourDomain!<br /><br />

This e-mail contains your LDAP username and password, which are required to access most protected company resources such as svn, development, stats, et al.<br /><br />

Please check with your supervisor if you have any questions regarding access rights or permissions.<br /><br />
% else:
Your password was reset as requested...<br /><br />
% endif

These credentials are for your own personal use only.<br /><br />

** DO NOT, UNDER ANY CIRCUMSTANCES, SHARE THIS INFORMATION WITH OTHERS **
<br /><br />

username: ${c.username}<br />
password: ${c.password}<br /><br />

Your personal VPN package can be downloaded <a href="https://vpnclient.yourdomain/">here</a>.<br />
Please login using the above credentials.<br /><br />

For any technical questions or issues please contact <a href="mailto:ops@yourdomain">ops@yourdomain</a>.
  </body>
</html>
