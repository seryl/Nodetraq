<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript">
    function removeStudio(id) {
        if (confirm("Are you sure you want to remove the Studio ${c.studio.name}?")) {
            location = "${h.url(controller='nodes', action='destroy_studio', id=c.studio.id)}";
        }
    }
</script>
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='show_studio', id=c.studio.id)}">Show</a>
</div>

<div style="float: right; margin-right: 2em;" class="box remove_item center">
    <a href="#" onClick="removeStudio(${c.studio.id});">Remove this studio</a>
</div>

<h2>${c.header}</h2>

${h.form(url(controller='nodes', action='update_studio', id=c.studio.id), method='POST')}
Name:<br />
${h.text('name', value=c.studio.name)} <br />
Description:<br />
${h.textarea('description', rows=10, cols=40, content=c.studio.description)} <br /> <br />
${h.submit(None, 'Submit')}
${h.end_form()}
