<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='network', action='edit', id=c.network_device.id)}">Edit this device</a>
</div>

<h2>Network Device</h2>
<div id="node">
    <table class="attributes">
        <tbody>
        </tbody>
        <tr>
            <th class="hostname">Hostname:</th>
            <td class="attr_hostname_tag">${c.network_device.hostname or '-'}</td>
            <th class="attr_logical">Logical:</th>
            <td class="attr_logical">${bool(c.network_device.logical)}</td>
        </tr>
        <tr>
            <th class="attr_management_ip">Management Ip:</th>
            <td class="attr_management_ip">
              ${c.network_device.management_ip or '-'}
            </td>
            <th class="attr_type">Type:</th>
            <td class="attr_type">${c.network_device.type or '-'}</td>
        </tr>
        <tr>
            <th class="attr_server_id">Part Number:</th>
            <td class="attr_server_id">${c.network_device.part_number or '-'}</td>
            <th class="attr_created">Created:</th>
            <td class="attr_created">
              % if c.network_device.created_at:
              ${c.network_device.created_at.strftime("%m/%d/%y")}
              % endif
            </td>
        </tr>
        <tr>
            <th class="attr_mac_address">Mac Address:</th>
            <td class="attr_mac_address">
              ${h.str_to_mac(c.network_device.mac_address) or '-'}
            </td>
            <th class="attr_updated">Updated:</th>
            <td class="attr_updated">
              % if c.network_device.updated_at:
              ${c.network_device.updated_at.strftime("%m/%d/%y")}
              % endif
            </td>
        </tr>
        % if c.network_device.parent:
        <tr>
          <th></th>
          <td></td>
          <th>Parent:</th>
          <td class="attr_parent">
            <a href="${h.url(controller='network', action='show', id=c.network_device.parent.id)}">${c.network_device.parent.hostname}</a>
          </td>
        </tr>
        % endif
    </table>
    <br />
</div>

% if not c.network_device.logical:
<!-- List of Network Device Children -->
<table class="list">
  <thead>
    <tr>
      <th><a href="">Hostname</a></th>
      <th><a href="">Management IP</a></th>
      <th><a href="">Type</a></th>
      <th><a href="">Serial No.</a></th>
      <th><a href="">Part No.</a></th>
    </tr>
  </thead>
  <tbody>
    % for i,child in enumerate(c.network_device.children):
    <tr class="${i%2 and 'even' or 'odd'}">
      <td class="hostname">
        <a href="${h.url(controller='network', action='show', id=child.id)}">${child.hostname}</a>
      </td>
      <td class="management_ip">${child.management_ip}</td>
      <td class="device_type">${child.type}</td>
      <td class="serial_no">${child.serial_number}</td>
      <td class="part_no">${child.part_number}</td>
    </tr>
    % endfor
  </tbody>
</table>
% endif
