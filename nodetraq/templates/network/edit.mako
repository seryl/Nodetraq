<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<meta name="device_id" content="${c.network_device.id}" />
<script type="text/javascript" src="/js/network.js"></script>
<script type="text/javascript">
  $(function() {
  update_parent_class();
  });
</script>
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='network', action='show', id=c.network_device.id)}">Show this device</a>
</div>

<div style="float: right; margin-right: 2em;" class="box remove_item center">
    <a href="#" onClick="removeDevice(${c.network_device.id});">Remove this device</a>
</div>

${h.form(url(controller='network', action='update', id=c.network_device.id))}
<h2>Network Device</h2>
<div id="node">
    <table class="attributes">
      <tbody>
      </tbody>
      <tr>
        <th class="hostname">Hostname:</th>
        <td class="attr_hostname_tag">
          ${h.text('_hostname', c.network_device._hostname)}
        </td>
        <th class="attr_logical">Logical:</th>
        <td class="attr_logical">${h.checkbox('logical', value=1, checked=bool(c.network_device.logical), onClick="update_parent_class();")}</td>
      </tr>
      <tr>
        <th class="attr_management_ip">Management Ip:</th>
        <td class="attr_management_ip">
          ${h.text('management_ip', value=c.network_device.management_ip)}
        </td>
        <th class="attr_type">Type:</th>
        <td class="attr_type">${h.text('type', c.network_device.type)}</td>
      </tr>
      <tr>
        <th class="attr_mac_address">Mac Address:</th>
        <td class="attr_mac_address">
          ${h.text('mac_address', h.str_to_mac(c.network_device.mac_address))}
        </td>
        <th class="attr_created">Created:</th>
        <td class="attr_created">
          % if c.network_device.created_at:
          ${c.network_device.created_at.strftime("%m/%d/%y")}
          % endif
        </td>
      </tr>
      <tr>
        <th class="attr_part_number">Part Number:</th>
        <td class="attr_part_number">
          ${h.text('part_number', value=c.network_device.part_number)}
        </td>
        <th class="attr_updated">Updated:</th>
        <td class="attr_updated">
          % if c.network_device.updated_at:
          ${c.network_device.updated_at.strftime("%m/%d/%y")}
          % endif
        </td>
      </tr>
      <tr>
        <th class="attr_serial_number">Serial Number:</th>
        <td class="attr_serial_number">
          ${h.text('serial_number', value=c.network_device.serial_number)}
        </td>
        <th class="attr_parent hidden">Parent:</th>
        <td class="attr_parent hidden">
          ${h.select('parent', 0, c.parents, onchange='')}
        </td>
      </tr>
    </table>
    <br />
</div>

<div class="align-right">
  <input type="button" onClick="UpdateNetworkDevice()" value="Submit" />
</div>

${h.end_form()}
