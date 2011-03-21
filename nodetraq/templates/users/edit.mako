<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link rel="stylesheet" type="text/css" href="/css/users.css" />
<script type="text/javascript" src="/js/users.js"></script>
<script type="text/javascript" src="/js/jquery.simplemodal-1.3.5.min.js"></script>
<meta name="username" content="${c.user['uid'][0]}" />
</%def>

<div style="margin: 0 auto; width: 1000px;">
  <h3>Editing existing user ${c.user['uid'][0]}</h3>
  <hr />

  <input type="hidden" id="username" value="${c.user['uid'][0]}" />
  <div id="user_information">
    % if c.user['nsAccountLock'][0].lower() == 'true':
    <div id="disabled_user_warning">This account has been disabled.</div>
    % endif
    <table width="100%">
      <thead>
      </thead>
      <tbody>
        <tr>
          <td width="15%">Full Name:</td>
          <td width="30%">${h.text('cn', value=c.user['cn'][0])}</td>
          <td width="10%"></td>
          <td width="15%">UID:</td>
          <td width="30%">${h.text('uidNumber', value=c.user['uidNumber'][0], disabled=True)}</td>
        </tr>
        <tr>
          <td width="15%">Email Address:</td>
          <td width="30%">${h.text('mail', value=c.user['mail'][0])}</td>
          <td width="10%"></td>
          <td width="15%">Login Shell:</td>
          <td width="30%">
            ${h.select('loginShell', c.user['loginShell'][0], [
            ('/bin/bash', '/bin/bash'),
            ('/bin/tcsh', '/bin/tcsh'),
            ('/bin/zsh', '/bin/zsh'),
            ('/sbin/nologin', '/sbin/nologin')
            ])}
          </td>
        </tr>
        <tr>
          <td width="15%">Title:</td>
          % if c.user.has_key('title'):
          <td width="30%">${h.text('title', value=c.user['title'][0])}</td>
          % else:
          <td width="30%">${h.text('title', value='')}</td>
          % endif
          <td width="10%"></td>
          <td width="15%">Department:</td>
          % if c.user.has_key('departmentNumber'):
          <td width="30%">${h.text('departmentNumber', value=c.user['departmentNumber'][0])}</td>
          % else:
          <td width="30%">${h.text('departmentNumber', value='')}</td>
          % endif
        </tr>
        <tr>
          <td width="15%">Manager:</td>
          % if c.user.has_key('manager'):
          <td width="30%">${h.text('manager', value=c.user['manager'][0])}</td>
          % else:
          <td width="30%">${h.text('manager', value='')}</td>
          % endif
          <td width="10%"></td>
          <td width="15%">Location:</td>
          % if c.user.has_key('roomNumber'):
          <td width="30%">${h.text('roomNumber', value=c.user["roomNumber"][0])}</td>
          % else:
          <td width="30%">${h.text('roomNumber', value='')}</td>
          % endif
        </tr>
        <tr>
          <td width="15%">Attributes:</td>
          <td width="30%">
            <div id="attributes_select">
              ${h.select("attributes_selections", 0, [
              ("", ""),
              ("orgchartmanager_div", "Org Chart Manager"),
              ("deploycode_div", "Deploy Code"),
              ("utilityaccount_div", "Utility Account")], onchange="update_shown_attrib()")}
            </div>
          </td>
          <td width="10%"></td>
          <td width="15%"></td>
          <td width="30%"></td>
        </tr>
        <tr>
          <td width="15%"></td>
          <td width="30%">
            <div id="orgchartmanager_div" style="display: none;">
              ${h.radio("orgchartmanager", "true", (c.user["orgchartmanager"][0] == 'true'), "True")}
              ${h.radio("orgchartmanager", "false", (c.user["orgchartmanager"][0] == 'false'), "False")}
            </div>
            <div id="deploycode_div" style="display: none;">
              ${h.radio("deploycode", "true", (c.user["deploycode"][0] == 'true'), "True")}
              ${h.radio("deploycode", "false", (c.user["deploycode"][0] == 'false'), "False")}
            </div>
            <div id="utilityaccount_div" style="display: none;">
              ${h.radio("utilityaccount", "true", (c.user["utilityaccount"][0] == 'true'), "True")}
              ${h.radio("utilityaccount", "false", (c.user["utilityaccount"][0] == 'false'), "False")}
            </div>
          </td>
          <td width="10%"></td>
          <td width="15%"></td>
          <td width="30%"></td>
        </tr>
      </tbody>
    </table>
    <div class="clear" style="margin: 12px;"></div>

    <table width="100%">
      <thead>
      </thead>
      <tbody>
        <tr>
          <td width="45%">Available groups:</td>
          <td width="10%"></td>
          <td width="45%">Groups this user is a member of:</td>
        </tr>
        <tr>
          <td width="45%">
            ${h.select('available_groups', 0, c.available_groups,
            multiple=True, style="width: 100%", size=7)}
          </td>
          <td width="10%">
            <div style="margin: 0 auto; width: 40px;">
              <input type="button" name="group_add" value=">>" onClick="addGroups();" />
              <br />
              <input type="button" name="group_del" value="<<" onClick="delGroups();" />
            </div>
          </td>
          <td width="45%">
            ${h.select('member_groups', 0, c.group_membership,
            multiple=True, style="width: 100%", size=7)}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <br />
  <input type="button" value="Submit Changes" onClick="submitChanges();" />
  <hr style="margin-top: 12px;"/>

  <table width="100%">
    <thead>
    </thead>
    <tbody>
      <tr>
        <td>New password:</td>
        <td>${h.password('new_password', value='')}</td>
        <td>Confirm:</td>
        <td>${h.password('confirm_password')}</td>
        <td>
          <input type="button" onClick="changePassword();" value="Change Password" />
        </td>
        % if c.user['nsAccountLock'][0] == 'true':
        <td style="float: right">
          <input type="button" onClick="enableUser();" value="Enable" />
        </td>
        % else:
        <td style="float: right">
          <input type="button" onClick="disableUser();" value="Disable" />
        </td>
        % endif
        <td style="float: right">
          <!--<input type="button" onClick="renameUser();" value="Rename" /> -->
        </td>
      </tr>
      <tr>
        <td colspan="4">
          <input type="button" onClick="resetPassword();" value="Reset Password" />
        </td>
      </tr>
    </tbody>
  </table>
</div>
