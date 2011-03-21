$TTL 86400
$ORIGIN yourdomain.com.
@   IN  SOA ns1.yourdomain.com. ns2.yourdomain.com. (
                        ${c.time} ;
                        120 ;
                        60 ;
                        1209600 ;
                        10800 )
        IN  NS  ns1.yourdomain.com.
        IN  NS  ns2.yourdomain.com.

% for node in c.nodes:
    % if node.primary_ip:
${node.hostname}        IN  A   ${node.primary_ip}
    % endif
    % if node.secondary_ip:
${node.hostname}.sec        IN  A   ${node.secondary_ip}
    % endif
    % if node.drac_ip:
${node.hostname}.drac     IN  A   ${node.drac_ip}
    % endif
    % for vhost in node.vhosts:
${vhost.hostname}        IN  CNAME   ${node.hostname}
    % endfor
% endfor

% for group in c.groups:
    % for node in group.nodes:
        % if group.name[:4] == 'www-':
${group.name[4:]}.group        IN  A   ${node.primary_ip}
        % else:
${group.name}.group        IN  A   ${node.primary_ip}
        % endif
    % endfor
% endfor
