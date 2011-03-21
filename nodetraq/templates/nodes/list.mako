<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%namespace file="/common/filters.mako" import="build_filterlist" />
<%def name="head_tags()">
    <link href="/css/jquery-ui.css" rel="stylesheet" type="text/css" />
    <script type="text/javascript" src="/js/jquery-ui-1.8.4.custom.min.js"></script>
    <script type="text/javascript" src="/js/jquery-ui-timepicker-addon-0.5.min.js"></script>
    <script type="text/javascript" src="/js/jquery.simplemodal-1.3.5.min.js"></script>
    <script type="text/javascript">
    $(function() {
        update_options();
        $('#tr_hostname').attr('style', '');
        $('#cb_hostname').attr('checked', 'true');
        toggle_filter('hostname');
        $('#add_filter_select option[value="hostname"]').attr('disabled', 'disabled');
        $('#tr_primary_ip').attr('style', '');
        $('#cb_primary_ip').attr('checked', 'true');
        toggle_filter('primary_ip');
        $('#add_filter_select option[value="primary_ip"]').attr('disabled', 'disabled');
        $('#values_hostname').focus();   
    });
    $('.list input[type="checkbox"]:checked').each(function() {
        ($(this).parent().parent().addClass('context-menu-selection'));
        });
    </script>
</%def>

% if c.selected_page == 'groups':
<div id="split_content_right" class="box center">
    <a href="${h.url(controller='groups', action='edit', id=c.group.id)}">Edit this group</a>
</div>
% endif
<h2>${c.header}</h2>

<div class="node_list">

${h.form(url(controller="nodes", action="index"),'get', id='query_form', name='query_form')}
<div id="query_form_content">
    <fieldset id="filters" class="collapsible">
        <legend onclick="toggleFieldset(this);">Filters</legend>
        <div style="">
        <table width="100%">
        <tbody>
        <tr>
            <td class="add-filter">
                Add filter:
                <select id="add_filter_select" class="select-small" onchange="add_filter();">
                    <option value=""></option>
                    % for filter in c.filters:
                    <option value="${filter['name']}">${filter['label']}</option>
                    % endfor

                </select>
            </td>

            <td>
                <input type="submit" style="display: none;" />
                <table style="border-collapse: collapse; border: 0pt none;">
                    <%call expr="build_filterlist(c.filters)"></%call>
                </table>
            </td>
        </tr>
        </tbody>
        </table>
    </div>
    </fieldset>

    <fieldset id="options" class="collapsible collapsed">
        <legend onclick="toggleFieldset(this);">Options</legend>
        <div style="display: none;">
            <table width="100%">
            <tbody>
            <tr>

                <td style="width: 150px;">
                    ${h.select('function', 0, [
                        ('edit_flags', 'Edit Flags'),
                        ('clear_flags', 'Clear Flags'),
                        ('add_group', 'Add to group'),
                        ('remove_group', 'Remove from group'),
                        ('update_game', 'Update Game'),
                        ('add_lb', 'Add to LB'),
                        ('enable_nagios', 'Enable Nagios'),
                        ('disable_nagios', 'Disable Nagios'),
                        ('enable_puppet', 'Enable Puppet'),
                        ('disable_puppet', 'Disable Puppet'),
                        ('nagios_options', 'Nagios Options'),
                        ('batch_edit', 'Batch Edit'),
                        ('export_csv', 'Export to CSV'),
                    ], onchange="update_options();")}
                </td>

                <td style="width: 200px;">
                    ${h.checkbox('cb_add_group', 'add_group', onclick='remove_filters();')}
                <label for="cb_add_group">Function</label>
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
${h.end_form()}

<table class="list">
<thead>
    <tr>
    <th><a class="check_toggle" href="javascript:toggle_checked()"><img src="../images/toggle_check.png" alt="Toggle_check" /></a></th>
    <th><a href="${h.generate_sort(c.request_url, c.sort_order, 'hostname')}">Hostname</a></th>
    <th><a href="${h.generate_sort(c.request_url, c.sort_order, 'service_tag')}">Service Tag</a></th>
    <th><a href="">Server ID</a></th>
    <th><a href="${h.generate_sort(c.request_url, c.sort_order, 'primary_ip')}">Primary IP</a></th>
    <th><a href="${h.generate_sort(c.request_url, c.sort_order, 'drac_ip')}">Drac IP</a></th>
    <th><a href="${h.generate_sort(c.request_url, c.sort_order, 'rack')}">Rack</a></th>
    <th><a href="${h.generate_sort(c.request_url, c.sort_order, 'rack_u')}">Rack U</a></th>
    <th><a href="">Groups</a></th>
    <th><a href="${h.generate_sort(c.request_url, c.sort_order, 'nagios')}">Nagios</a></th>
    <th><a href="${h.generate_sort(c.request_url, c.sort_order, 'puppet')}">Puppet</a></th>
    </tr>
</thead>
<tbody>
% for i, node in enumerate(c.nodes):
    <tr class="${i%2 and 'even' or 'odd'}">
    <td class="checkbox">
        <input class="ShiftCheckbox" type="checkbox" name="${node.id}" value="${node.id}" />
    </td>
    <td class="hostname"><a href="${h.url(controller='nodes', action='show', id=node.id)}">${node.hostname}</a></td>
    <td class="service_tag">${node.service_tag}</td>
    <td class="server_id">${node.server_id}</td>
    <td class="primary_ip">${node.primary_ip}</td>
    <td class="drac_ip">${node.drac_ip}</td>
    <td class="rack">${node.rack}</td>
    <td class="rack_u">${node.rack_u}</td>
    <td class="groups">
    <% last_group = len(node.groups)-1 %>
    % for i, group in enumerate(node.groups):
        % if (i == last_group):
        <a href="${h.url(controller='groups', action='show', id=group.id)}">${group.name}</a>
        % else:
        <a href="${h.url(controller='groups', action='show', id=group.id)}">${group.name}</a>, 
        % endif
        % if (i != 0 and (i+1) % 3 == 0):
        <br />
        % endif
    % endfor
    </td>
    <td class="nagios ${node.nagios and 'enabled' or 'disabled'}"></td>
    <td class="puppet ${node.puppet and 'enabled' or 'disabled'}"></td>
    </tr>
% endfor
</tbody>
</table>

<p class="pagination">
<%call expr="generate_pagination(c.page, c.total_pages, c.current_page_count, c.node_count, c.link_append)"></%call>
</p>

</div>

<div class="break"></div>
