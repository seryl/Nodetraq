% for group in c.groups:
GROUP:${group.name}
    % for node in group.nodes:
${node.hostname} ${str(node.nagios)}
    % endfor
% endfor
GROUP:all
% for node in c.nodes:
${node.hostname} ${str(node.nagios)}
% endfor
