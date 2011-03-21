<%def name="show_comments(comments)">
% for comment in comments:
<div class="display_comment" id="comment_${comment.id}">
    % if comment.user.name == c.current_user['username']:
    <div class="comment_mod"><a href="${h.url(controller='nodes', action='edit_comment', id=c.node.id, commentid=comment.id)}">Edit</a> | <a href="${h.url(controller='nodes', action='destroy_comment', id=c.node.id, commentid=comment.id)}">Delete</a></div>
    % endif
  <table>
    <tr>
      <td>
        <span class="gravatar">${h.gravatar(comment.user.email, size=40)}</span>
      </td>
      <td>
        <span class="username"><p><a href="">${comment.user.name}</a></p>
        <span class="date">${comment.created_at.date()}</span></span>
      </td>
      <td style="padding-left: 26px;">
        <p>${h.literal(h.markdown(comment.description))}</p>
      </td>
    </tr>
  </table>
</div>
% endfor
</%def>
