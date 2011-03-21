
% if c.active_user['user_level'] == 0:
<h3>Nodes</h3>
<ul class="no-dec">
    % if not c.subpage == 'list':
    <li>
        <a href="${h.url(controller='nodes', action='index')}">List nodes</a>
    </li>
    % endif
    % if not c.subpage == 'new':
    <li>
        <a href="${h.url(controller='nodes', action='new')}">New Node</a>
    </li>
    % endif
    % if not c.subpage == 'importcsv':
    <li>
        <a href="${h.url(controller='nodes', action='importcsv')}">Import csv</a>
    </li>
    % endif
</ul>
% endif

<h3>Database Backups</h3>
<ul class="no-dec">
  <li><a href="${h.url(controller='nodes', action='show_dbbackups')}">List Backups</a></li>
</ul>

<h3>Studios</h3>
<ul class="no-dec">
  <li><a href="${h.url(controller='nodes', action='create_studio')}">Create Studio</a></li>
  <li><a href="${h.url(controller='nodes', action='list_studios')}">List Studios</a></li>
</ul>

<h3>Games</h3>
<ul class="no-dec">
  <li><a href="${h.url(controller='nodes', action='create_game')}">Create Game</a></li>
  <li><a href="${h.url(controller='nodes', action='list_games')}">List Games</a></li>
</ul>

