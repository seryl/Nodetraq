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

<div class="record_publish">
  <table>
    <thead>
    </thead>
    <tbody>
      <tr>
        <td id="diff_id">
        </td>
      </tr>
      <tr>
        <td>
          <input type="button" onClick="publish_record();" value="Publish" />
        </td>
      </tr>
    </tbody>
  </table>
</div>
