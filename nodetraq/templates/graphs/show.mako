<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%namespace file="/common/filters.mako" import="build_filterlist" />
<%def name="head_tags()">
% if c.graph:
    <meta content="${c.graph.filename[1:]}" name="current_graph" />
    <meta content="${c.graph.name}" name="graph_name" />
% endif
    <script type="text/javascript">
      function update_graph_iframe() {
          var graph = $("#chosen_graph").val();
          var iframe = $("iframe")[0];
          if (graph) {
              $(iframe).attr("src", "https://graphs.yourdomain/cgi-bin/drraw.cgi?Mode=view;Graph=" + graph);
          } else {
              $(iframe).attr("src", "https://graphs.yourdomain/cgi-bin/drraw.cgi");
          }
          iframe.contentWindow.location.reload(true);
      }

      $(function () {
          var selected_graph = $("meta[name='current_graph']").attr("content");
          if (selected_graph) {
              $("#chosen_graph").val(selected_graph);
          }
      });
    </script>
</%def>

<div style="width: 100%; display: block; text-align: center;">
  <select id="chosen_graph", onchange="update_graph_iframe();">
    <option></option>
    % for graph in c.graph_list:
    <option value="${graph.filename[1:]}">${graph.name}</option>
    % endfor
  </select>
</div>

% if c.graph:
<iframe class="nodec-iframe" src="https://graphs.yourdomain/cgi-bin/drraw.cgi?Mode=view;Graph=${c.graph.filename[1:]}" width="100%" height="600px;">
  <p>Your browser does not support iframes.</p>
</iframe>
% else:
<iframe class="nodec-iframe" src="https://graphs.yourdomain/cgi-bin/drraw.cgi" width="100%" height="600px;">
  <p>Your browser does not support iframes.</p>
</iframe
% endif
