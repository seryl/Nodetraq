$TTL 86400
$ORIGIN 10.in-addr.arpa.
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
${h.rbind(node.primary_ip)}        IN  PTR   ${node.hostname}.yourdomain.com.
    % endif
    % if node.secondary_ip:
${h.rbind(node.secondary_ip)}        IN  PTR   ${node.hostname}.sec.yourdomain.com.
    % endif
    % if node.drac_ip:
${h.rbind(node.drac_ip)}     IN  PTR   ${node.hostname}.drac.yourdomain.com.
    % endif
% endfor

