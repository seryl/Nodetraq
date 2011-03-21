<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<h2>Create New Pool</h2>

${h.form(url(controller='loadbalancer', action='createpool'), method='POST')}
Name:<br />
${h.text('pool')}
${h.submit(None, 'Submit')}
${h.end_form()}

