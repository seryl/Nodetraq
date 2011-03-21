<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link href="/css/dns.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="/js/dns.js"></script>
<meta name="domain" value="${c.domain}" />
</%def>

<div class="record_modify">
<h2>Host: ${h.text('host', '')}</h2>
  <table>
    <thead>
    </thead>
    <tbody>
      <tr datatype="selector">
        <td>
          Record Type: 
          ${h.select('record_type', 'a', [
          ('a', 'a'),
          ('cname', 'cname'),
          ('mx', 'mx'),
          ('txt', 'txt'),
          ('ptr', 'ptr'),
          ], onchange="update_record_type();")}
        </td>
      </tr>
      <tr>
        <td datatype="result" count="0">
          ip: ${h.text('ip', '')}
          ttl: ${h.text('ttl', '')}
        </td>
        <td>
          <a href="javascript:remove_result(0);">remove</a>
        </td>
      </tr>
      <tr class="align-right" datatype="addnew">
        <td style="padding-top: 24px;">
          <a href="javascript:add_new_result();">Add new</a>
        </td>
      </tr>
      <tr class="align-right">
        <td style="padding-top: 24px;">
          <input type="button" value="Submit" onClick="SubmitRecord();" />
        </td>
      </tr>
    </tbody>
  </table>
</div>
