<%inherit file="/common/base.mako" />
<%def name="head_tags()">
</%def>

<h2>Activity : Info</h2>
% if c.activity.activity_type.name == 'node':
<%include file="/activity/display/nodelist.mako" />

% endif
<%doc>
% for changeset in c.activity.changesets:
    % if changeset.new_value:
    <h4>Changeset</h4>
    <p>${changeset.field}</p>
    <p>${changeset.old_value} ->
    ${changeset.new_value}</p>
    % else:
    <p><label>${changeset.field}</label>
    ${changeset.old_value}</p>
    % endif
% endfor
</%doc>
<div class="break"></div>
