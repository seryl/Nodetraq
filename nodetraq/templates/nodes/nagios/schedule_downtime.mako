${h.form(url(controller='nagios', action='schedule_host_downtime', method='post'))}
<div style="text-align: center; font-weight: bold;">Schedule downtime</div>
<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>Start Time: </td>
      <td><input id="start_time" value="${h.nagios_current_time()}"></input></td>
    </tr>
    <tr>
      <td>End Time: </td>
      <td><input id="end_time"></input></td>
    </tr>
    <tr>
      <td>Comment: </td>
      <td>${h.textarea('comment', cols=23, rows=6)}</td>
    </tr>
    <tr>
      <td class="align-right" colspan=2>
        <br />
        <input type="button" onClick="call_schedule_downtime();" value="Submit">
      </td>
    </tr>
  </tbody>
</table>

${h.end_form()}
