<%page args="activity=None" />
% if activity:
    % if not activity.children:
    <%call expr="render_changesets(activity.changesets)"></%call>
    % else:
        % for child in activity.children[:3]:
        <%call expr="render_changesets(child.changesets)"></%call>
        % endfor
    % endif
% endif

<%def name="render_changesets(changeset)">
<%
    order = {}
    importance = ('hostname', 'primary_ip')
    for change in changeset:
        if change.field in importance:
            order[change.field] = {'old': change.old_value, 'new': change.new_value}

    has_blockquote = False
%>
    % for item in importance:
        % if order.has_key(item):
            % if item == 'hostname':
                % if order[item]['new']:
            <p class="hostname">${order[item]['old']} -> ${order[item]['new']}</p>
                % else:
            <p class="hostname">${order[item]['old']}</p>
                % endif
            <blockquote>
            % endif
            % if order[item]['new']:
    <label>${item}: </label>${order[item]['old']} -> ${order[item]['new']}<br />
            % else:
    <label>${item}: </label>${order[item]['old']}<br />
            % endif
        % endif
    % endfor
    </blockquote>
</%def>

