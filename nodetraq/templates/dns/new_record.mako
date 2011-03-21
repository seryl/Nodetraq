<tr>
  <td datatype="result" count="${c.count}">
    % if c.record_type == 'a':
    ip: ${h.text('ip', '')}
    ttl: ${h.text('ttl', '')}
    % elif c.record_type == 'cname':
    domain: ${h.text('domain', '')}
    ttl: ${h.text('ttl', '')}
    % elif c.record_type == 'mx':
    domain: ${h.text('domain', '')}
    ttl: ${h.text('ttl', '')}
    % elif c.record_type == 'txt':
    text: ${h.textarea('text', '', cols=35, rows=4 )}
    ttl: ${h.text('ttl', '')}
    % elif c.record_type == 'ptr':
    domain: ${h.text('domain', '')}
    ttl: ${h.text('ttl', '')}
    % endif
  </td>
  <td>
    <a href="javascript:remove_result(${c.count});">remove</a>
  </td>
</tr>
