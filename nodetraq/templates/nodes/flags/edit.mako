${h.form(url(controller='nodes', action='update_flags', method='post'))}
<input type="hidden" name="user" value="${c.user}" />
<div style="float: left">
Description: <br/ >
${h.textarea('description', cols=29, rows=5)}
</div>
<div style="float: right">
Flags:
<div style="margin-top: 6px;">
% for flag in c.flags:
<input type="checkbox" name="${flag.name}" value="${flag.name}" />
<label for="${flag.name}">${flag.name}</label><br />
% endfor
</div>
</div>
<div class="break"></div>
<input type="button" onClick="call_update_flags();" value="Update">
${h.end_form()}
