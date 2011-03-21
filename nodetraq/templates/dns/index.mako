<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link href="/css/dns.css" rel="stylesheet" type="text/css" />
</%def>

<div id="dns_list">
  <table class="list">
    <thead>
      <tr>
        <th id="dns_type">Type</th>
        <th id="dns_host">Host</th>
        <th id="dns_results">Results</th>
      </tr>
    </thead>
    <tbody>
      % for i, record in enumerate(c.records):
      <tr id="${record._record_type}_${record.host}" class="${i%2 and 'even' or 'odd'}">
        <td class="record_type">${record._record_type}</td>
        <td class="record_host">${record.host}</td>
        <td class="record_results">
          <div class="result_set">
            % for result in record.results:
            <div class="result">
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
            </div>
            % endfor
          </div>
        </td>
      <tr/>
      % endfor
    </tbody>
  </table>
</div>
