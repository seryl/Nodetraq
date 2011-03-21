% if not c.node_flag_info:
<tr>
  <td style="text-align: center;">
    None
  </td>
</tr>
% else:
% for i, info in enumerate(c.node_flag_info):
<tr>
  <td class="flag_td">
    <a class="flag_host" title="${h.render_flag_info(info)}" href="${h.url(controller='nodes', action='show', id=info.node.id)}">${info.node.hostname}</a> &ndash; <span class="flag_user">${info.user.name}</span>
    <div class="flag_list">
      % for flag in info.flags:
      <span class="flag_list_${flag.name}"></span>
      % endfor
    </div>
    <div class="flag_description">${info.description}</div>
    <div class="clear"></div>
  </td>
</tr>
% endfor
% endif
