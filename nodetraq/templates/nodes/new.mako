<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

${h.form(h.url(controller='nodes', action='create'), method='post')}

<div class="new_node">
  <table>
    <thead>
      <tr>
        <th colspan=2>New Node</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Hostname: </td>
        <td>${h.text('hostname', size=31)}<td>
      </tr>
      <tr>
        <td>Service Tag: </td>
        <td>${h.text('service_tag', size=31)}</td>
      </tr>
      <tr>
        <td>Primary IP: </td>
        <td>${h.text('primary_ip', size=31)}</td>
      </tr>
      <tr>
        <td>Location: </td>
        <td>${h.text('location', size=31)}</td>
      </tr>
      <tr>
        <td>Description: </td>
        <td style="padding-top: 10px;">${h.textarea('description', rows=8, cols=30)}</td>
      </tr>
      <tr>
        <td class="align-right" colspan=2>
          <br />
          ${h.submit('node_submit', None)}
        </td>
      </tr>
    </tbody>
  </table>
</div>

${h.end_form()}

<div class="break"></div>
