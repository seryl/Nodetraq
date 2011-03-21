<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link href="/css/dns.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="/js/dns.js"></script>
<meta name="domain" value="${c.domain}" />
</%def>

<div id="dns_list">
  <table class="list">
    <thead>
      <tr>
        <th id="dns_type">Type</th>
        <th id="dns_host">Host</th>
        <th id="dns_results">Results</th>
        <th id="dns_edit">Edit</th>
      </tr>
    </thead>
    <tbody>
      % for i, record in enumerate(c.records):
      <tr id="${record._record_type}_${record.host}" class="${i%2 and 'even' or 'odd'}" type="${record._record_type}" host="${record.host}">
        <td class="record_type">${record._record_type}</td>
        <td class="record_host">${record.host}</td>
        <td class="record_results">
          <div class="result_set">
            % for result in record.results:
            <div class="result">
              <span type="result">
                % if result._result_type == 'a':
                <span type="ip">${result.ip}</span> ttl=<span type="ttl">${result.ttl}</span>
                % elif result._result_type == 'cname':
                <span type="domain">${result.domain}</span> ttl=<span type="ttl">${result.ttl}</span>
                % elif result._result_type == 'mx':
                <span type="domain">${result.domain}</span> preference=<span type="preference">${result.preference}</span> ttl=<span type="ttl">${result.ttl}</span>
                % elif result._result_type == 'ptr':
                <span type="domain">${result.domain}</span> ttl=<span type="ttl">${result.ttl}</span>
                % elif result._result_type == 'txt':
                <span type="text">${result.text}</span> ttl=<span type="ttl">${result.ttl}</span>
                % endif
              </span>
            </div>
            % endfor
          </div>
        </td>
        <td class="record_edit">
          <a href="${h.url(controller='dns', action='edit_record', domain=c.domain, type=record._record_type)}${record.host}">Edit</a>
        </td>
      <tr/>
      % endfor
      <tr class="additional_options" id="add_dns_record">
        <td colspan=3></td>
        <td class="hostname" style="padding: 10px 0px;">
          <a href="${url(controller='dns', action='add_record')}">Add Record</a>
        </td>
      </tr>
    </tbody>
  </table>
</div>
