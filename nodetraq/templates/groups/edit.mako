<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript">
    function removeGroup(id) {
        if (confirm("Are you sure you want to remove the group ${c.group.name}?")) {
            location = "${h.url(controller='groups', action='destroy', id=c.group.id)}";
        }
    }
</script>
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='groups', action='show', id=c.group.id)}">Show this group</a>
</div>
<div style="float: right; margin-right: 2em;" class="box remove_item center">
    <a href="#" onClick="removeGroup(${c.group.id});">Remove this group</a>
</div>
<div class="break"></div>

<div id="edit_group">
${h.form(h.url(controller='groups', action='update'), method='post')}
<table>
  <thead>
    <tr>
      <th colspan=2>Editing: ${c.group.name}</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Name: </td>
      <td>${h.text('name', value=c.group.name, size=31)}</td>
    </tr>
    <tr>
      <td>Description: </td>
      <td>${h.textarea('description', content=c.group.description, rows=6, cols=30)}</td>
    </tr>
    <tr>
      <td colspan=2 class="align-right">${h.submit('Submit', None)}</td>
    </tr>
  </tbody>
</table>
${h.hidden('group_id', c.group.id)}
${h.end_form()}
</div>
<div class="break"></div>
