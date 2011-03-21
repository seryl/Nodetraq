% for comment in comments
<div class="comment">
    ${h.gravatar(comment.user.email)}
    ${comment.user.name}
    ${comment.description}
</div>
% endfor
