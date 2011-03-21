<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%namespace file="/common/filters.mako" import="build_filterlist" />
<%def name="head_tags()">
</%def>

${h.form(url(controller='graphs', action='create'))}

<div id="graph_menu">

  <table width="100%">
    <thead>
    </thead>
    <tbody>
      <tr class="align-center">
        <td colspan=3 style="padding-bottom: 10px;">
          <label for="graph_title">Graph Title: </label>
          ${h.text("graph_title", id="graph_title")}
        </td>
      </tr>
      <tr class="align-center">
        <td colspan=3 style="padding-bottom: 10px;">
          <label for="group_select">Group: </label>
          <select name="group_select" id="group_select" onChange="">
            % for group in c.groups:
            <option value="${group.name}">${group.name}</option>
            % endfor
          </select>
        </td>
      </tr>
      <tr class="align-left">
        % for i, rrd_type in enumerate(c.rrd_types):
        % if (i) % 3 == 0 and i:
      </tr>
      <tr class="align-left">
        % endif
        <td>
        ${h.checkbox('rrd_type', value=rrd_type, label=rrd_type)}
        </td>
        % endfor
      </tr>
      <tr class="align-center">
        <td colspan=3 style="padding-top: 20px;">
          ${h.submit(None, 'Submit')}
        </td>
      </tr>
    </tbody>
  </table>

</div>

${h.end_form()}
