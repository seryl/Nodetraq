<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link rel="stylesheet" type="text/css" href="/css/simpletooltip.css" />
<script type="text/javascript" src="/js/jquery.tooltip.v.1.1.js"></script>

<script type="text/javascript">
    function removeNode(id) {
        if (confirm("Are you sure you want to remove the node ${c.node.hostname}?")) {
            location = "${h.url(controller='nodes', action='destroy', id=c.node.id)}";
        }
    }
</script>
<script type="text/javascript" langeuage="javascript">
  function check_sync(ele, attrib) {
      if (ele.attr('reported') != ele.attr('real')) {
          ele.siblings("th[class='" + attrib + "']")
              .addClass('sync_issue_highlight');
      }
  }

  $(function() {
  var hostname = $("h2[item='hostname']");

  var primary_ip = $("#node td[class='attr_primary_ip']");
  var primary_mac = $("#node td[class='attr_primary_mac']");
  var secondary_ip = $("#node td[class='attr_secondary_ip']");
  var secondary_mac = $("#node td[class='attr_secondary_mac']");

  if (hostname.attr('reported') != hostname.attr('real')) {
      hostname.addClass('sync_issue_highlight');
  }
  check_sync(primary_ip, "attr_primary_ip");
  check_sync(primary_mac, "attr_primary_mac");
  check_sync(secondary_ip, "attr_secondary_ip");
  check_sync(secondary_mac, "attr_secondary_mac");

  $(".info_hover").simpletooltip();

  });
</script>
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='show', id=c.node.id)}">Show this node</a>
</div>
<div style="float: right; margin-right: 2em;" class="box remove_item center">
    <a href="#" onClick="removeNode(${c.node.id});">Remove this node</a>
</div>

${h.form(url(controller='nodes', action='update', method='post', id=c.node.id))}
<h2 item="hostname" reported="${c.node.reported_hostname}" real="${c.node.hostname}">Hostname: ${h.text('hostname', value=c.node.hostname, title=c.node.reported_hostname or 'None', class_='info_hover')} : ${c.node.model_name}</h2>

<div id="node">
    <table class="attributes edit-attr">
        <tbody>
        </tbody>
        <tr>
            <th class="attr_service_tag">Service Tag:</th>
            <td class="attr_service_tag">${h.text('service_tag', value=c.node.service_tag)}</td>
            <th class="attr_primary_ip">Primary Ip:</th>
            <td class="attr_primary_ip" reported="${c.node.reported_primary_ip}" real="${c.node.primary_ip}">
              ${h.text('primary_ip', value=c.node.primary_ip, title=c.node.reported_primary_ip or 'None', class_='info_hover')}
            </td>
        </tr>
        <tr>
            <th class="attr_location">Location:</th>
            <td class="attr_location">${h.text('location', value=c.node.location)}</td>
            <th class="attr_primary_mac">Primary MAC</th>
            <td class="attr_primary_mac" reported="${c.node.reported_primary_mac}" real="${h.str_to_mac(c.node.primary_mac)}">
              ${h.text('primary_mac', value=c.node.primary_mac, title=c.node.reported_primary_mac or 'None', class_='info_hover')}
            </td>
        </tr>
        <tr>
            <th class="attr_server_id">Server Id:</th>
            <td class="attr_server_id">${c.node.server_id}</td>
            <th class="attr_secondary_ip">Secondary Ip:</th>
            <td class="attr_secondary_ip" reported="${c.node.reported_secondary_ip}" real="${c.node.secondary_ip}">
              ${h.text('secondary_ip', value=c.node.secondary_ip, title=c.node.reported_secondary_ip or 'None', class_='info_hover')}
            </td>
        </tr>
        <tr>
            <th class="attr_rack">Rack:</th>
            <td class="attr_rack">${h.text('rack', value=c.node.rack)}</td>
            <th class="attr_secondary_mac">Secondary MAC:</th>
            <td class="attr_secondary_mac" reported="${c.node.reported_secondary_mac}" real="${h.str_to_mac(c.node.secondary_mac)}">
              ${h.text('secondary_mac', value=c.node.secondary_mac, title=c.node.reported_secondary_mac or 'None', class_='info_hover')}
            </td>
        </tr>
        <tr>
            <th class="attr_rack_u">Rack U:</th>
            <td class="attr_rack_u">${h.text('rack_u', value=c.node.rack_u)}</td>
            <th class="attr_drac_ip">Drac:</th>
            <td class="attr_drac_ip">${h.text('drac_ip', value=c.node.drac_ip)}</td>
        </tr>
        <tr>
          <th class="attr_server_license">Server Lic:</th>
          <td class="attr_server_license">${h.text('server_license', value=c.node.server_license)}</td>
          <th class="attr_drac_switch">Drac Switch:</th>
          <td class="attr_drac_switch">${h.text('drac_switch', value=c.node.drac_switch)}</td>
        </tr>
        <tr>
          <th class="attr_sql_license">Sql Lic:</th>
          <td class="attr_sql_license">${h.text('sql_license', value=c.node.sql_license)}</td>
          <th class="attr_drac_port">Drac Port:</th>
          <td class="attr_drac_port">${h.text('drac_port', value=c.node.drac_port)}</td>
        </tr>
        <tr>
            <th class="attr_xen_instance">Xen:</th>
            <td class="attr_xen_instance">${h.text('xen_instance', value=c.node.xen_instance)}</td>
            <th class="attr_nagios">Nagios:</th>
            <td class="attr_nagios">
                ${h.radio('nagios', 1, c.node.nagios, 'Enabled')}
                ${h.radio('nagios', 0, not c.node.nagios, 'Disabled')}
            </td>
        </tr>
        <tr>
            <th class="attr_created_at">Created:</th>
            <td class="attr_created_at">${c.node.created_at.date()}</td>
            <th class="attr_game">Game</th>
            <td class="attr_game">${h.select('game', c.selected_game, c.game_list)}</td>
        </tr>
    </table>
<p>
    <strong>Description:</strong>
</p>
${h.textarea('description', value=c.node.description, rows=8, cols=60)}
<hr />
% if c.node.updated_at:
Updated: ${c.node.updated_at.strftime("%m/%d/%y %H:%M")} <br />
% endif
<br />
Firmware: ${c.node.firmware} <br />
Root Password: ${c.node.root_password} <br />

vhosts (<a href="${h.url(controller='vhosts', action='index', id=c.node.id)}">edit</a>):
<? last_vhost = len(c.node.vhosts)-1 %>
% for i, vhost in enumerate(c.node.vhosts):
% if (i == last_vhost):
    ${vhost.hostname}
% else:
    ${vhost.hostname},
% endif
% endfor
<br />
db backups (<a href="${h.url(controller='dbbackups', action='index', id=c.node.id)}">edit</a>):
<? last_db_backup = len(c.node.db_backups)-1 %>
% for i, db_backup in enumerate(c.node.db_backups):
% if (i == last_db_backup):
    ${db_backup.server.hostname}
% else:
    ${db_backup.server.hostname},
% endif
% endfor
<br />

<h2>Hardware</h2>
Processor: ${c.node.cpu_processor}<br />
CPU Count: ${c.node.cpu_count} <br />
Memory: ${c.node.memory} GB<br /><br />

Groups:
<% last_group = len(c.node.groups)-1 %>
% for i, group in enumerate(c.node.groups):
    % if (i == last_group):
    <a href="${h.url(controller='groups', action='show', id=group.id)}">${group.name}</a> 
    % else:
    <a href="${h.url(controller='groups', action='show', id=group.id)}">${group.name}</a>, 
    % endif
% endfor
<br /><br />

ssh rsa:<br />
${h.textarea('ssh_key', c.node.ssh_key, rows=8, cols=60)} <br /><br />

ssh dsa:<br />
${h.textarea('puppet_key', c.node.puppet_key, rows=8, cols=60)} <br /><br />
</div>

<span style="float: right; margin-right: 30px;">
${h.submit(None, 'Submit')}
</span>

${h.end_form()}
<div class="break"></div>

<div class="comments-list">
</div>
<!--
<div class="new-comment">
    ${h.form(url(controller='nodes', action='comment', id=c.node.id))}
    ${h.textarea('comment', rows=4, cols=40)} <br />
    ${h.submit(None, 'Submit')}
    ${h.end_form()}
</div>
-->
