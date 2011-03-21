<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<script type="text/javascript" language="javascript">
  function create_studio() {
    data = {
            'name': $("#name").val(),
            'description': $("#description").val()
           };
    $.ajax({
      type: 'POST',
      url: "${h.url(controller='nodes', action='new_studio')}",
      data: JSON.stringify(data),
      success: function(data) {
        window.location = "${h.url(controller='nodes', action='list_studios')}";
      }
    });
  }
</script>
</%def>

<div id="split_content_right" class="box center">
    <a href="${h.url(controller='nodes', action='list_studios')}">List Studios</a>
</div>

<h2>${c.header}</h2>

Name: ${h.text('name')} <br />
Description: <br />
${h.textarea('description', rows=10, cols=40)} <br /> <br />
<button onClick="create_studio();">Submit</button>
