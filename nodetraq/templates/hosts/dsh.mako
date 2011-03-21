% for group in c.groups:
GROUP:${group.name}
    % for node in group.nodes:
${node.hostname}
    % endfor
% endfor
GROUP:all
% for node in c.nodes:
${node.hostname}
% endfor
