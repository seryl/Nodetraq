<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link rel="stylesheet" type="text/css" href="/css/users.css" />
<script type="text/javascript" src="/js/users.js"></script>
<script type="text/javascript" src="/js/jquery.simplemodal-1.3.5.min.js"></script>
<meta name="groupname" content="${c.group['cn'][0]}" />
</%def>

<div style="margin: 0 auto; width: 1000px;">
  <h3>Editing existing group ${c.group['cn'][0]}</h3>
  <hr />

  <div id="new_group_form">
    <div style="width: 600px; margin: 0 auto;">
      <table> 
        <thead> 
        </thead> 
        <tbody>
          <tr>
            <td>${h.hidden('group', value=c.group['cn'][0])}</td>
            <td></td>
          </tr>
          <tr> 
            <td>Group name: </td> 
            <td>
              ${h.text('cn', value=c.group['cn'][0])}
            </td> 
          </tr> 
          <tr> 
            <td>Description: </td> 
            <td>
              % if c.group.has_key("description"):
              ${h.textarea('description', content=c.group['description'][0], rows=6, cols=30)}
              % else:
              ${h.textarea('description', content="", rows=6, cols=30)}
              % endif
            </td> 
          </tr> 
          <tr> 
            <td colspan=2 class="align-right"><input id="none" type="submit" value="Update" onClick="submitGroupChanges();" /></td> 
          </tr> 
        </tbody> 
      </table>
      <div class="clear" style="margin: 12px;"></div>
    </div>

</div>

<hr style="margin-top: 12px;" />
