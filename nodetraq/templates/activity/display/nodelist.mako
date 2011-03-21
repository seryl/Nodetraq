<h3>${c.activity.link}</h3>
% if c.activity.children:
    % for child in c.activity.children:
        <%call expr="show_single(child)"></%call>
    % endfor
% else:
    <%call expr="show_single(c.activity)"></%call>
% endif

<%def name="show_single(activity)">
    <div class="box">
        <blockquote>
        % for changeset in activity.changesets:
            % if changeset.new_value:
        <p>${changeset.field}</p>
        <p>${changeset.old_value} -> ${changeset.new_value}</p>
            % else:
        <p><label>${changeset.field}</label>
        ${changeset.old_value}</p>
            % endif
        % endfor
        </blockquote>
    </div>
</%def>

