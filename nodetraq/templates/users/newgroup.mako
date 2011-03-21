<%inherit file="/common/base.mako" />
<%def name="head_tags()">
<link rel="stylesheet" type="text/css" href="/css/users.css" />
<script type="text/javascript" src="/js/users.js"></script>
<script type="text/javascript" src="/js/jquery.simplemodal-1.3.5.min.js"></script>
</%def>

<div style="margin: 0 auto; width: 1000px;">
  <h3>Creating new group</h3>
  <hr />

${h.form(url(controller='users', action='creategroup'), method='post')}
  <div id="new_group_form">
    <div style="width: 600px; margin: 0 auto;">
      <table> 
        <thead> 
        </thead> 
        <tbody> 
          <tr> 
            <td>Group name: </td> 
            <td>
              ${h.text('name')}
            </td> 
          </tr> 
          <tr> 
            <td>Description: </td> 
            <td>
              ${h.textarea('description', rows=6, cols=30)}
            </td> 
          </tr> 
          <tr> 
            <td colspan=2 class="align-right">
              ${h.submit(None, 'Submit')}
          </tr> 
        </tbody> 
      </table>
      <div class="clear" style="margin: 12px;"></div>
    </div>
${h.end_form()}

</div>

<hr style="margin-top: 12px;" />
