<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%namespace file="/common/filters.mako" import="build_filterlist" />
<%def name="head_tags()">
</%def>

<div id="graph_list">
  <div class="align-center">
    <h2>Current Graphs</h2>
  </div>
  <table class="list">
    <thead>
      <tr>
        <th>Name</th>
        <th>Rrd</th>
        <th>Filename</th>
        <th>Edit</th>
      </tr>
    </thead>
    <tbody>
      % for i, graph in enumerate(c.graphs):
      <tr class="${i%2 and 'even' or 'odd'}">
        <td class="align-center">
          <a href="${h.url(controller='graphs', action='show', id=graph.name)}">${graph.name}</a>
        </td>
        <td class="align-center">
          <a href="${h.url(controller='graphs', action='rrd_file', id=graph.name)}">rrd</a>
        </td>
        <td class="align-center">
          ${graph.filename}
        </td>
        <td class="align-center">
          <a href="${h.url(controller='graphs', action='edit', id=graph.name)}">edit</a>
        </td>
      </tr>
      % endfor
    </tbody>
  </table>
  <br />
  <div class="align-center" style="font-size: 80%;">
    <a href="${h.url(controller='graphs', action='new')}">Create New Graph</a>
  </div>
</div>

