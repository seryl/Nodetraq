<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<div style="margin: 0 auto; padding: 0 140px;">
<h3>Network Devices</h3>
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
  % for i,device in enumerate([d for d in c.network_devices if not d.logical]):
  <tr class="${i%2 and 'even' or 'odd'}">
    <td class="hostname">
      <a href="${h.url(controller='network', action='show', id=device.id)}">${device.hostname}</a>
    </td>
    <td class="management_ip">${device.management_ip}</td>
    <td class="device_type">${device.type}</td>
    <td class="serial_no">${device.serial_number}</td>
    <td class="part_no">${device.part_number}</td>
  </tr>
  % endfor
</tbody>
</table>
<br />

<h3>Logical Devices</h3>
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
  % for i, device in enumerate([d for d in c.network_devices if d.logical]):
  <tr class="${i%2 and 'even' or 'odd'}">
    <td class="hostname">
      <a href="${h.url(controller='network', action='show', id=device.id)}">${device.hostname}</a>
    </td>
    <td class="management_ip">${device.management_ip}</td>
    <td class="device_type">${device.type}</td>
    <td class="serial_no">${device.serial_number}</td>
    <td class="part_no">${device.part_number}</td>
  </tr>
  % endfor
</tbody>
</table>
</div>
