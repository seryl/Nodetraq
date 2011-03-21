<div id="top-menu">
    <div id="account">
        % if c.active_user:
            <div id="loggedas">
                Logged in as <a href="#">${c.active_user['username']}</a>
            </div>
            <!--<a href="/my_account">My account</a>-->
            <a href="/logout">Sign out</a>
        % else:
            <a href="/login">Sign in</a>
        % endif
    </div>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/help">Help</a></li>
    </ul>
</div>
<div id="header">
    <!--
    <div id="quick_search">
        ${h.form(h.url(controller='search', action='index'), method='get')}
        Search: ${h.text('search')}
        ${h.end_form()}<br />
    </div>
    -->
    <h1>Nodetraq</h1>
    <div class="break"></div>
    <div id="main-menu">
        <ul>
          % if c.active_user['user_level'] == 0:
            <li><a class='dashboard' href="${h.url(controller='dashboard', action='index')}">Dashboard</a></li>
            <li><a class='activity' href="${h.url(controller='activity', action='index')}">Activity</a></li>
            <li><a class='groups' href="${h.url(controller='groups', action='index')}">Groups</a></li>
            <li><a class='nodes' href="${h.url(controller='nodes', action='index')}">Nodes</a></li>
            <!--
            <li><a class="network" href="${h.url(controller='network', action='index')}">Network</a></li>
            -->
            <li><a class='users' href="${h.url(controller='users', action='search')}">Users</a></li>
            <li><a class='graphs' href="${h.url(controller='graphs', action='index')}">Graphs</a></li>
            <!--
            <li><a class='loadbalancer' href="${h.url(controller='loadbalancer', action='index')}">LB</a></li>
            -->
            <!--<li><a class='inventory' href="${h.url(controller='inventory', action='index')}">Inventory</a></li>-->
            <!--<li><a class='news' href="/news">News</a></li>-->
            <!--<li><a class='wiki' href="/wiki">Wiki</a></li>-->
            <!--<li><a class='tools' href="/tools">Tools</a></li>-->
            <li><a class='dns' href="/dns">DNS</a></li>
            % elif c.active_user['user_level'] == 10:
            <li><a class='nodes' href="${h.url(controller='nodes', action='show_dbbackups')}">Database</a></li>
            % endif
            <li><a class='pools' href="/pools">Pools</a></li>
        </ul>
    </div>
    <div class="break"></div>
</div>
<div class="break"></div>

