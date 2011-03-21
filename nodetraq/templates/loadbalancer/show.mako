<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%def name="head_tags()">
    <script type="text/javascript">
    $(function() {
        toggleFieldset($('#options legend'));
        update_options();
    });
    function removePool() {
        if (confirm("Are you sure you want to remove the pool ${c.members[0]}?")) {
            location = "/loadbalancer/deletepool?pools[]=${c.members[0]}";
        }
    }
    </script>
</%def>

<div id="split_content_right" class="box remove_item center">
    <a href="#" onClick="removePool();">Remove this pool</a>
</div>

<h2>${c.members[0]}</h2>

${h.form(url(controller='loadbalancer', action="index"), 'GET', id='query_form', name='query_form')}
<div id="query_form_content">
    <fieldset id="options" class="collapsible collapsed">
        <legend onclick="toggleFieldset(this);">Options</legend>
        <div style="display: none;">
            <table width="100%">
            <thead>
            </thead>
            <tbody>
            <tr>
                <td style="width: 200px;">
                    ${h.checkbox('cb_add_group', 'add_group', onclick='remove_filters();', checked="True")}
                <label for="cb_add_group">Function</label>
                </td>

                <td style="width: 150px;">
                    ${h.select('function', 0, [
                        ('enable_host', 'Enable Host'),
                        ('disable_host', 'Disable Host'),
                        ('remove_lb', 'Remove from LB'),
                    ], onchange="update_options();")}
                </td>

                <td id="options_info" style="display: none;">
                </td>

                <td class="selected_secondary">
                </td>
            </tr>
            </tbody>
            </table>
        </div>
    </fieldset>
</div>

<p class="buttons">
    <a class="icon icon-checked" onclick="apply_function();" href="#">Apply</a>
    <a class="icon icon-reload" onclick="clear_checked();" href="#">Clear</a>
    <span style="float: right;">${h.checkbox('show_all', True)}<label for="show_all">Show All</label></span>
</p>
<input type="hidden" name="pool" value="${c.members[0]}">
${h.end_form()}

<table class="list">
<thead>
    <tr>
        <th><a class="check_toggle" href="javascript:toggle_checked()">${h.image('../../images/toggle_check.png', alt="Toggle Check")}</th>
        <th><a href="">Hostname</a></th>
        <th><a href="">Port</a></th>
        <th><a href="">Enabled</a></th>
    </tr>
</thead>
<tbody>
% for i,node_mapping in enumerate(c.members[1]):
    <tr class="${i%2 and 'even' or 'odd'}">
        <td class="checkbox">
            <input class="ShiftCheckbox" type="checkbox" name="${node_mapping[0].id}" value="${node_mapping[0].id}">
        </td>
        <td class="hostname"><a href="${h.url(controller='nodes', action='show', id=node_mapping[0].id)}">${node_mapping[0].hostname}</a></td>
        <td class="port">${node_mapping[1]}</td>
        <td class="${node_mapping[2] and 'enabled' or 'disabled'}"></td>
    </tr>
% endfor
</tbody>
</table>

