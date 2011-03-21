<%inherit file="/common/base.mako" />
<%def name="head_tags()">
    <link type="application/atom+xml" title="ATOM" rel="alternate" href="${h.url(controller='activity', action='atom')}">
</%def>
<% import datetime
earlier = c.end_date - datetime.timedelta(days=3)
later = c.end_date + datetime.timedelta(days=3)
%>

<h2>Activity</h2>
<p class="subtitle">From ${c.start_date} to ${c.end_date}</p>

<div id="activity">
<%
    cur_date = None
    old_date = None
%>
% for activity in c.activities:
    % if h.now().date() == activity.created_at.date():
    <% 
        if not cur_date:
            cur_date = activity.created_at.date()
    %>
        % if old_date != cur_date:
<h3 id="${activity.created_at.date()}">Today</h3>
    <% old_date = cur_date %>
        % endif
    % else:
    <%
        if not cur_date:
            cur_date = activity.created_at.date()
        elif cur_date != activity.created_at.date():
            cur_date = activity.created_at.date()
    %>
        % if cur_date != old_date:
<h3 id="${activity.created_at.date()}">${activity.created_at.date()}</h3>
        % endif
    <% old_date = cur_date %>
    % endif
<dl>
    <dt class="${activity.activity_type.name}-${activity.activity_type.action}-activity">
        <span class="time">${activity.created_at.strftime("%H:%M")}</span>
        <a href="${h.url(controller='activity', action='info', id=activity.id)}">${activity.link}</a>
    </dt>
    <dd>
    <span class="description">
    % if activity.activity_type.name == 'node':
    <%include file="/activity/display/abbr_nodelist.mako", args="activity=activity" />
    % elif activity.activity_type.name == 'group':
    <%include file="/activity/display/abbr_grouplist.mako", args="activity=activity" />
    % elif activity.activity_type.name == 'loadbalancer':
    lol
    % elif activity.activity_type.name == 'inventory':
    <%include file="/activity/display/abbr_inventorylist.mako", args="activity=activity" />
    % endif
    </span>
    <span class="author">${activity.user.name}</span>
    </dd>
</dl>

% endfor
</div>

<div style="float: left;">
    <a href="">&laquo Previous</a>
</div>

% if last_page:
<div style="float: right;">
    <a href="">Next &raquo</a>
</div>
% endif
<div class="break"></div>

<p class="other-formats">
    Also available in:
    <span>
        <a class="atom" rel="nofollow" href="${h.url(controller='activity', action='atom')}">Atom</a> | <a href="${h.url(controller='activity', action='index', format='json')}">JSON</a> | <a href="${h.url(controller='activity', action='index', format='xml')}">XML</a>
    </span>
</p>

<div class="break"></div>

