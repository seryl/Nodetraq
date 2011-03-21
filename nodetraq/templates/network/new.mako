<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript" src="/js/network.js"></script>
<script type="text/javascript">
  $(function() {
  update_parent_class();
  });
</script>
</%def>

${h.form(url(controller='network', action='create'))}
<h2>Network Device</h2>
<div id="node">
    <table class="attributes">
        <tbody>
        </tbody>
        <tr>
          <th class="hostname">Hostname:</th>
          <td class="attr_hostname_tag">
            ${h.text('_hostname')}
          </td>
          <th class="attr_logical">Logical:</th>
          <td class="attr_logical">${h.checkbox('logical', value=1, onClick='update_parent_class()')}</td>
        </tr>
        <tr>
          <th class="attr_management_ip">Management Ip:</th>
          <td class="attr_management_ip">
            ${h.text('management_ip')}
          </td>
          <th class="attr_type">Type:</th>
          <td class="attr_type">${h.text('type')}</td>
        </tr>
        <tr>
          <th class="attr_mac_address">Mac Address:</th>
          <td class="attr_mac_address">
              ${h.text('mac_address')}
          </td>
          <th></th>
          <td></td>
        </tr>
        <tr>
          <th class="attr_part_number">Part Number:</th>
          <td class="attr_part_number">
            ${h.text('part_number')}
          </td>
          <th></th>
          <td></td>
        </tr>
        <tr>
          <th class="attr_serial_number">Serial Number:</th>
          <td class="attr_serial_number">
            ${h.text('serial_number')}
          </td>
          <th class="attr_parent hidden">Parent:</th>
          <td class="attr_parent hidden">
            ${h.select('test', 0, c.parents, onchange='')}
          </td>
        </tr>
    </table>
    <br />
</div>

<div class="align-right">
  <input type="button" onClick="CreateNetworkDevice()" value="Submit" />
</div>

${h.end_form()}
