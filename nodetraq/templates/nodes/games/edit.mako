<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript">
    function removeGame(id) {
        if (confirm("Are you sure you want to remove the Game ${c.game.name}?")) {
            location = "${h.url(controller='nodes', action='destroy_game', id=c.game.id)}";
        }
    }
</script>
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='show_game', id=c.game.id)}">Show</a>
</div>

<div style="float: right; margin-right: 2em;" class="box remove_item center">
    <a href="#" onClick="removeGame(${c.game.id});">Remove this studio</a>
</div>

<h2>${c.header}</h2>

${h.form(url(controller='nodes', action='update_game', id=c.game.id), method='POST')}
Name:<br />
${h.text('name', value=c.game.name)} <br />
Studio: ${h.select('studio', c.selected_studio, c.studio_list)} <br />
Description:<br />
${h.textarea('description', rows=10, cols=40, content=c.game.description)} <br /> <br />
${h.submit(None, 'Submit')}
${h.end_form()}
