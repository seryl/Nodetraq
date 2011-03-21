<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%namespace file="/common/filters.mako" import="build_filterlist" />
<%def name="head_tags()">
% if c.graph:
    <meta content="${c.graph.group.name}" name="selected_group" />
% else:
    <meta content="" name="selected_group" />
% endif
    <script type="text/javascript">
      function update_selected_group() {
          var group = $("meta[name='selected_group']").attr("content");
          console.log(group);
      }

      $(function() {
          update_selected_group();
      });
    </script>
</%def>

${h.form(url(controller='graphs', action='update'))}

<input type="hidden" value="${c.graph.id}" name="id" />
<input type="hidden" value="${c.graph.filename}" name="filename" />
<div id="graph_menu">

  <table width="100%">
    <thead>
    </thead>
    <tbody>
      <tr class="align-center">
        <td colspan=3 style="padding-bottom: 10px;">
          <label for="graph_title">Graph Title: </label>
          ${h.text("graph_title", id="graph_title", value=c.graph.name)}
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
          % if rrd_type in c.graph.get_rrds():
          ${h.checkbox('rrd_type', value=rrd_type, label=rrd_type, checked=True)}
          % else:
          ${h.checkbox('rrd_type', value=rrd_type, label=rrd_type)}
          % endif
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
