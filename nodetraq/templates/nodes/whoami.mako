REMOTE_ADDR=${c.ip}
% if c.node:
XEN_VM=${c.node.xen_instance}
HOSTNAME=${c.node.hostname}
SERVERID=${c.node.server_id}
PRIMARY_IP=${c.node.primary_ip}
SECONDARY_IP=${c.node.secondary_ip}
PRIMARYMAC=${c.node.primary_mac}
SECONDARY_MAC=${c.node.secondary_mac}
DRAC_IP=${c.node.drac_ip}
% for i,group in enumerate(c.node.groups):
SECONDARY_GROUP${i+1}=${group}
% endfor
% endif

