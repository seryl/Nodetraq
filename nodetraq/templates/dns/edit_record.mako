<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link href="/css/dns.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="/js/dns.js"></script>
<meta name="domain" value="${c.domain}" />
<meta name="host" value="${c.record.host}" />
</%def>

<div style="float: right; margin-right: 2em;" class="box remove_item center">
  <a href="javascript:remove_dns_record('${c.record._record_type}', '${c.record.host}')">Remove this record</a>
</div>

<div class="record_modify">
  <h2>${c.record._record_type}: ${c.record.host}</h2>
  <table>
    <thead>
    </thead>
    <tbody>
      <tr datatype="selector">
        <td>
          ${h.hidden('record_type', c.record._record_type)}
        </td>
        <td>
        </td>
      </tr>
      <tr>
        <td>
        </td>
        <td>
        </td>
      </tr>
      % for i, result in enumerate(c.record.results):
      <tr>
        <td datatype="result" count="${i}">
          % if c.record._record_type == 'a':
          ip: ${h.text('ip', result.ip)}
          ttl: ${h.text('ttl', c.record.results[0].ttl)}
          % elif c.record._record_type == 'cname':
          domain: ${h.text('domain', c.record.results[0].domain)}
          ttl: ${h.text('ttl', c.record.results[0].ttl)}
          % elif c.record._record_type == 'mx':
          domain: ${h.text('ip', c.record.results[0].domain)}
          ttl: ${h.text('ttl', c.record.results[0].ttl)}
          % elif c.record._record_type == 'txt':
          text: ${h.textarea('text', c.record.results[0].text, cols=55, rows=6)}<br />
          ttl: ${h.text('ttl', c.record.results[0].ttl)}
          % elif c.record._record_type == 'ptr':
          domain: ${h.text('domain_name', c.record.results[0].domain)}
          ttl: ${h.text('ttl', c.record.results[0].ttl)}
          % endif
        </td>
        <td>
          <a href="javascript:remove_result(${i});">remove</a>
        </td>
      </tr>
      % endfor
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
