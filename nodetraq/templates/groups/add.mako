<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<div id="new_group">
    <h2>Add nodes to ${c.group.name}</h2>

    ${h.form(h.url(controller='groups', action='create'), method='post')}
    <div class="name">
    Name: ${h.text('name')}
    </div>
    <br />

    <div class="description">
    <div id="description_tag">Description:</div>
    <div id="description_form">${h.textarea('description', '', cols=40, rows=8)}</div>
    </div>
    <br />
    
    ${h.submit('group_submit', 'Submit')}
    ${h.end_form()}

</div>
<div class="break"></div>
