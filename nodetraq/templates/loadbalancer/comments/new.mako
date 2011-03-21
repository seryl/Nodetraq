<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%def name="head_tags()">
</%def>

<h2>Load balancer -- Comment</h2>

<div class="new-comment">
    ${h.form(url(controller='loadbalancer', action='createcomment', id=c.loadbalancer.id))}
    <input type="hidden" name="user_id" value="${c.user_id}"></input>
    <input type="hidden" name="pool" value="${c.pool}"></input>
    Comment:<br />
    ${h.textarea('comment')} <br />
    ${h.submit(None, 'Submit')}
    ${h.end_form()}
</div>

