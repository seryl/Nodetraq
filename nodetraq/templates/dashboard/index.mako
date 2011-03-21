<%inherit file="/common/base.mako" />
<%def name="head_tags()">
    <link rel="stylesheet" type="text/css" href="/css/simpletooltip.css" />
    <script type="text/javascript" src="/js/jquery.tooltip.v.1.1.js"></script>
    <script type="text/javascript" src="/js/jquery.ekko.js"></script>
    <script type="text/javascript">
      $(function() {
        $(".sync_info").simpletooltip();        

        
        $("#flagged_list").ekko({
          url: "/dashboard/display_flags"
        }, function(data) {
          $("#flagged_list tbody").html(data);
          $(".flag_host").simpletooltip();
        });

        /*
        $("#problem_list").ekko({
          url: "/dashboard/display_problems"
        }, function(data) {
          $("#problem_list tbody").html(data);
          $(".problem_info").simpletooltip();
        });
        */
      });
    </script>
    <script type="text/javascript" src="/js/rabbitmq.js"></script>
    <link type="application/atom+xml" title="ATOM" rel="alternate" href="${h.url(controller='dashboard', action='atom')}" />
</%def>

<div style="float: left; width: 31%; margin: 5px;">
<table id="flagged_list" class="list">
<thead>
    <tr>
        <th>Flagged Nodes</th>
    </tr>
</thead>
<tbody>
  <tr>
    <td style="text-align: center;">
      <img src="/images/loading.gif" /><br />Loading...
    </td>
  </tr>
</tbody>
</table>
</div>

<div style="float: left; width: 31%; margin: 5px;">
<table id="problem_list" class="list">
<thead>
    <tr>
        <th>Problems</th>
    </tr>
</thead>
<tbody>
  <tr>
    <td style="text-align: center;">
      <img src="/images/loading.gif" /><br />Loading...
    </td>
  </tr>
</tbody>
</table>
</div>

<div style="float: left; width: 31%; margin: 5px;">
<table id="sync_list" class="list">
<thead>
    <tr>
        <th>Sync Issues</th>
    </tr>
</thead>
<tbody>
  % for i, sync_issue in enumerate(c.sync_issues):
  <tr>
    <td class="sync_td">
      <a class="sync_info" title="${h.render_sync_issue(sync_issue)}" href="${h.url(
               controller='nodes', action='show',
               id=sync_issue['id'])}">${sync_issue['hostname']}</a>
    </td>
  </tr>
  % endfor
</tbody>
</table>
</div>

<div class="break"></div>

<p class="other-formats">
    Also available in
    <span>
        <a class="atom" href="${h.url(controller='dashboard', action='atom')}">Atom</a>
    </span>

</p>
<div class="break"></div>

