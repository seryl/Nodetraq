
<%inherit file="/common/base.mako" />
<%namespace file="/nodes/comments/_show.mako" import="show_comments" />
<%namespace file="/nodes/disks/_list.mako" import="show_disks" />
<%def name="head_tags()">
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

  });
</script>
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='edit', id=c.node.id)}">Edit this node</a>
</div>

<h2 item="hostname" reported="${c.node.reported_hostname}" real="${c.node.hostname}">${c.node.hostname} : ${c.node.model_name}</h2>

<div id="node">
    <table class="attributes">
        <tbody>
        </tbody>
        <tr>
            <th class="attr_service_tag">Service Tag:</th>
            <td class="attr_service_tag">${c.node.service_tag or '-'}</td>
            <th class="attr_primary_ip">Primary Ip:</th>
            <td class="attr_primary_ip" reported="${c.node.reported_primary_ip or '-'}" real="${c.node.primary_ip or '-'}">
              ${c.node.primary_ip or '-'}
            </td>
        </tr>
        <tr>
            <th class="attr_location">Location:</th>
            <td class="attr_location">${c.node.location or '-'}</td>
            <th class="attr_primary_mac" >Primary MAC</th>
            <td class="attr_primary_mac" reported="${c.node.reported_primary_mac or '-'}" real="${h.str_to_mac(c.node.primary_mac) or '-'}">
              ${h.str_to_mac(c.node.primary_mac) or '-'}
            </td>
        </tr>
        <tr>
            <th class="attr_server_id">Server Id:</th>
            <td class="attr_server_id">${c.node.server_id or '-'}</td>
            <th class="attr_secondary_ip">Secondary Ip:</th>
            <td class="attr_secondary_ip" reported="${c.node.reported_secondary_ip or '-'}" real="${c.node.secondary_ip or '-'}">
              ${c.node.secondary_ip or '-'}
            </td>
        </tr>
        <tr>
            <th class="attr_rack">Rack:</th>
            <td class="attr_rack">${c.node.rack or '-'}</td>
            <th class="attr_secondary_mac">Secondary MAC:</th>
            <td class="attr_secondary_mac" reported="${c.node.reported_secondary_mac or '-'}" real="${h.str_to_mac(c.node.secondary_mac) or '-'}">
              ${h.str_to_mac(c.node.secondary_mac) or '-'}
            </td>
        </tr>
        <tr>
            <th class="attr_rack_u">Rack U:</th>
            <td class="attr_rack_u">${c.node.rack_u}</td>
            <th class="attr_drac_ip">Drac:</th>
            <td class="attr_drac_ip">${c.node.drac_ip or '-'}</td>
        </tr>
        <tr>
          <th class="attr_server_license">Server Lic:</th>
          <td class="attr_server_license">${c.node.server_license or '-'}</td>
          <th class="attr_drac_switch">Drac Switch:</th>
          <td class="attr_drac_switch">${c.node.drac_switch or '-'}</td>
        </tr>
        <tr>
          <th class="attr_sql_license">Sql Lic:</th>
          <td class="attr_sql_license">${c.node.sql_license or '-'}</td>
          <th class="attr_drac_port">Drac Port:</th>
          <td class="attr_drac_port">${c.node.drac_port or '-'}</td>
        </tr>
        <tr>
            <th class="attr_xen_instance">Xen:</th>
            <td class="attr_xen_instance">${c.node.xen_instance or '-'}</td>
            <th class="attr_nagios">Nagios:</th>
            <td class="attr_nagios">${c.node.nagios and True or False}</td>
        </tr>
        <tr>
            <th class="attr_created_at">Created:</th>
            <td class="attr_created_at">${c.node.created_at.date()}</td>
            <th class="attr_game">Game</th>
            <td class="attr_game">${'-' if c.node.game == None else h.link_to(c.node.game.name, h.url(controller='nodes', action='show_game', id=c.node.game.id))}</td>
        </tr>
    </table>
<p>
    <strong>Description:</strong>
</p>
${c.node.description}
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

<h3>Disks</h3>
<%call expr="show_disks(c.node.disks)"></%call>
<br /><br />

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
<!-- 
ssh rsa:<br />
${h.textarea('ssh_key', c.node.ssh_key, rows=8, cols=60)}<br /><br />

ssh dsa:<br />
${h.textarea('puppet_key', c.node.puppet_key, rows=8, cols=60)}<br /><br />
-->
</div>

<div class="break"></div>

<div class="comments-list">
<h3>Comments</h3>
<%call expr="show_comments(c.node.comments)"></%call>
</div>

<h3>Add Comment</h3>
<div class="new-comment">
    ${h.form(url(controller='nodes', action='create_comment'))}
    ${h.hidden(name='node', value=c.node.id)}
    ${h.textarea('comment', rows=6, cols=60)} <br />
    ${h.submit(None, 'Submit')}
    ${h.end_form()}
</div>

