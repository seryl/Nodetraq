<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link href="/css/dns.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="/js/dns.js"></script>
<meta name="domain" value="${c.domain}" />
<script type="text/javascript">
  $(document).ready(function() {
    update_diffs();
  });
</script>
</%def>

<div class="record_revert">
  <h1>Revert</h1>
  <table>
    <thead>
    </thead>
    <tbody>
      <tr>
        <td>
          revision: ${h.select('revert_list', 0, c.rev_list, onchange="update_diffs();")}
        </td>
      </tr>
      <tr>
        <td id="diff_id">
        </td>
      </tr>
      <tr>
        <td>
          <input type="button" onClick="revert_record();" value="Revert" />
        </td>
      </tr>
    </tbody>
  </table>
</div>
