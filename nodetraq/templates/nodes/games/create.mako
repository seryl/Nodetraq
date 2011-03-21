<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript" language="javascript">
  function create_game() {
    data = {
            'name': $("#name").val(),
            'studio': parseInt($("#studio").val()),
            'description': $("#description").val()
           };
    $.ajax({
      type: 'POST',
      url: "${h.url(controller='nodes', action='new_game')}",
      data: JSON.stringify(data),
      success: function(data) {
        window.location = "${h.url(controller='nodes', action='list_games')}";
      }
    });
  }
</script>
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='list_games')}">List Games</a>
</div>

<h2>${c.header}</h2>

Name: ${h.text('name')} <br />
Studio: ${h.select('studio', 0, c.studios)} <br />
Description: <br />
${h.textarea('description', rows=10, cols=40)} <br /> <br />
<button onClick="create_game();">Submit</button>
