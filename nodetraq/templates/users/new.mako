<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link rel="stylesheet" type="text/css" href="/css/users.css" />
<script type="text/javascript" src="/js/users.js"></script>
<script type="text/javascript" src="/js/jquery.simplemodal-1.3.5.min.js"></script>
</%def>

<div style="margin: 0 auto; width: 1000px;">
  <h3>Creating new user</h3>
  <hr />

  <div id="user_information">
    <table width="100%">
      <thead>
      </thead>
      <tbody>
        <tr>
          <td width="15%">Username:</td>
          <td width="30%">${h.text('username')}</td>
          <td width="10%"></td>
          <td width="15%">Full Name:</td>
          <td width="30%">${h.text('name')}</td>
        </tr>
        <tr>
          <td width="15%">Email Address:</td>
          <td width="30%">${h.text('mail')}</td>
          <td width="10%"></td>
          <td width="15%">Login Shell:</td>
          <td width="30%">
            ${h.select('loginShell', '/sbin/nologin', [
            ('/bin/bash', '/bin/bash'),
            ('/bin/tcsh', '/bin/tcsh'),
            ('/bin/zsh', '/bin/zsh'),
            ('/sbin/nologin', '/sbin/nologin')
            ])}
          </td>
        </tr>
        <tr>
          <td width="15%">Title:</td>
          <td width="30%">${h.text('title', value='')}</td>
          <td width="10%"></td>
          <td width="15%">Department:</td>
          <td width="30%">${h.text('departmentNumber', value='')}</td>
        </tr>
        <tr>
          <td width="15%">Manager:</td>
          <td width="30%">${h.text('manager', value='')}</td>
          <td width="10%"></td>
          <td width="15%">Location:</td>
          <td width="30%">${h.text('roomNumber', value='')}</td>
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
              ${h.radio("orgchartmanager", "true", False, "True")}
              ${h.radio("orgchartmanager", "false", True, "False")}
            </div>
            <div id="deploycode_div" style="display: none;">
              ${h.radio("deploycode", "true", False, "True")}
              ${h.radio("deploycode", "false", True, "False")}
            </div>
            <div id="utilityaccount_div" style="display: none;">
              ${h.radio("utilityaccount", "true", False, "True")}
              ${h.radio("utilityaccount", "false", True, "False")}
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
            ${h.select('member_groups', 0, c.groups,
            multiple=True, style="width: 100%", size=7)}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <br />
  <input type="button" value="Create" onClick="createUser();" />
</div>
