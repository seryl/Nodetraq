<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

${h.form(url(controller='nodes', action='update_comment', id=c.node_id, commentid=c.comment.id), method='POST')}
${h.textarea('description', c.comment.description, rows=6, cols=60)} <br />
${h.submit(None, 'Submit')}
${h.end_form()}

