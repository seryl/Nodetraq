% for group in c.groups:
# ${group}
    % for node in c.groups[group]:
    % if c.nagios == 0 or c.nagios == 1:
        % if node.nagios == c.nagios:
${node.primary_ip} ${node.hostname} ${node.server_id}
        % endif
    % else:
${node.primary_ip} ${node.hostname} ${node.server_id}
    % endif
    % endfor

% endfor

