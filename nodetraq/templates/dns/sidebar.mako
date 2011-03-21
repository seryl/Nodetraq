<h3>DNS</h3>

<ul class="no-dec">
  <!--<li><a href="${url(controller='dns', action='index')}">Select Domain</a></li> -->
  <li><a href="${h.url(controller='dns', action='index', domain=c.domain)}">List</a></li>
  <li><a href="${url(controller='dns', action='add_record', domain=c.domain)}">Add Record</a></li>
</ul>
<br />

<ul class="no-dec">
  <li><a href="javascript:pull_production();">Pull Production Config</a></li>
</ul>
<br />

<ul class="no-dec">
  <li><a href="${url(controller='dns', action='revert', domain=c.domain)}">Revert</a></li>
  <li><a href="${url(controller='dns', action='publish', domain=c.domain)}">Publish</a></li>
</ul>
<br />
