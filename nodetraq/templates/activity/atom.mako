<?xml version="1.0" encoding="utf-8"?>
<% import datetime %>
<feed>

    <title>Nodetraq Activity Feed</title>
    <subtitle>Daily activity reports</subtitle>
    <link href="https://nodetraq/activity.atom" ref="self"/>
    % if c.activity:
    <updated>${(c.activity[0].created_at+datetime.timedelta(hours=7)).isoformat()[:-10]+'Z'}</updated>
    % else:
    <updated></updated>
    % endif
    <author>
        <name>Ops</name>
        <email>ops@yourdomain</email>
    </author>

    % for activity in c.activity:
    <entry>
        <title>${activity.link}</title>
        <link rel="alternate" href="https://localhost/activity/info/${activity.id}" />
        <updated>${(activity.created_at+datetime.timedelta(hours=7)).isoformat()[:-10]+'Z'}</updated>
        <content type="xhtml">
            % if activity.activity_type.name == 'node':
            <%call expr="node_content(activity)"></%call>
            % elif activity.activity_type.name == 'group':
            <%call expr="group_content(activity)"></%call>
            % else:
            <%call expr="inventory_content(activity)"></%call>
            % endif
        </content>
    </entry>
    % endfor

</feed>

<%def name="group_content(activity)">
% for child in activity.children:
${child}
% endfor
</%def>

<%def name="node_content(activity)">
% if activity.children:
% for child in activity.children:
    ${child}
% endfor
% else:
<%
important_vals = ('hostname', 'primary_ip')
cs_hash = {}
for cs in activity.changesets:
    cs_hash[cs.field] = {'old': cs.old_value, 'new': cs.new_value}
%>
% for imp in important_vals:
% if cs_hash.has_key(imp):
    % if cs_hash[imp]['new']:
    ${imp}: ${cs_hash[imp]['old'] or 'None'} -> ${cs_hash[imp]['new'] or 'None'}
    % else:
    ${imp}: ${cs_hash[imp]['old'] or 'None'}
    % endif
<%
del(cs_hash[imp])
%>
% endif
% endfor

% for cs in cs_hash:
${cs}: ${cs_hash[cs]['old'] or 'None'} -> ${cs_hash[cs]['new'] or 'None'}
% endfor
% endif
</%def>

<%def name="node_changesets(activity)">
% for a in activity:
    ${a}
% endfor
</%def>

<%def name="inventory_content(activity)">
inventory
</%def>
