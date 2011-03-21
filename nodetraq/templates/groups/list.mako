<%inherit file="/common/base.mako" />
<%namespace file="/common/pagination.mako" import="generate_pagination" />
<%namespace file="/common/filters.mako" import="build_filterlist" />
<%def name="head_tags()">
    <script type="text/javascript">
    $(function() {
        $('#tr_group').attr('style', '');
        $('#cb_group').attr('checked', 'true');
        toggle_filter('group');
        $('#add_filter_seelct option[value="group"]').attr('disabled', 'disabled');
        $('#values_group').focus();
    });
    $('.list input[type="checkbox"]:checked').each(function() {
        ($(this).parent().parent().addClass('context-menu-selection'));
        });
    </script>
</%def>

<h2>${c.heading}</h2>

<div id="group_list">
${h.form(url(controller='groups', action='index'), 'GET', id='query_form', name='query_form')}
<div id="query_form_content">
    <fieldset id="filters" class="collapsible">
        <legend onclick="toggleFieldset(this);">Filters</legend>
        <div style="">
        <table width="100%">
        <thead>
        </thead>
        <tbody>
        <tr>
            <td>
                <table style="border-collapse: collapse; border: 0pt none;">
                    <%call expr="build_filterlist(c.filters)"></%call>
                </table>
            </td>
        </tr>
        </tbody>
        </table>
        </div>
    </fieldset>
</div>

<p class="buttons">
    <a class="icon icon-checked" onclick="apply_function();" href="#">Apply</a>
    <span style="float: right;">${h.checkbox('show_all', True)}<label for="show_all">Show All</label></span>
</p>

${h.end_form()}

<table class="list">
    <thead>
    <tr>
        <th title="Group"><a href="">Group</a></th>
        <th title="Count"><a href="">Count</a></th>
        <th title="Desription"><a href="">Description</a></th>
    </tr>
    </thead>
    <tbody>
% for i, group in enumerate(c.groups):
    <tr class="${i%2 and 'even' or 'odd'}">
        <td class="group"><a href="${h.url(controller='groups', action='show', id=group.name)}">${group.name}</a></td>
        <td class="count">${len(group.nodes)}</td>
        <td class="description"><a href="${h.url(controller='groups', action='edit', id=group.id)}">${group.description}</a></td>
    </tr>
    </tbody>
% endfor
</table>

<p class="pagination">
<%call expr="generate_pagination(c.page, c.total_pages, c.current_page_count, c.group_count, c.link_append)"></%call>
</p>

</div>
<div class="break"></div>

