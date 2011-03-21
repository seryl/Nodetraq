<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<h2>Comment</h2>

${h.form(url(controller='dashboard', action='createflag'))}
${h.hidden('fnode_id', c.fnode_id)}
${h.select('flag', selected_values = [], options = c.flag_list)} <br />
${h.textarea('description', rows=6, cols=60)} <br />
${h.submit(None, 'Submit')}
${h.end_form()}
