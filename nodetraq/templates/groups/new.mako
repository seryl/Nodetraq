<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<div id="new_group">
    ${h.form(h.url(controller='groups', action='create'), method='post')}

    <table>
      <thead>
        <tr>
          <th>New Group</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Name: </td>
          <td>${h.text('name', size=31)}</td>
        </tr>
        <tr>
          <td>Description: </td>
          <td>${h.textarea('description', '', cols=30, rows=8)}</td>
        </tr>
        <tr>
          <td colspan=2 class="align-right" style="padding-top: 10px">
            ${h.submit('group_submit', 'Submit')}
          </td>
        </tr>
      <tbody>
    </table>

    ${h.end_form()}
</div>
<div class="break"></div>
