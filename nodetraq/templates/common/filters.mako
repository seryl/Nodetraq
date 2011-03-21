
<%def name="build_filterlist(filters)">
% for filter in filters:
<tr id="tr_${filter['name']}" class="filter" style="display: none;">
    <td style="width: 200px;">
        ${h.checkbox(id="cb_"+filter['name'], value=filter['name'], onclick="toggle_filter('"+filter['name']+"')", name="fields[]")}
        <label for="cb_${filter['name']}">${filter['label']}</label>
    </td>
    <td style="width: 150px;">
        % if filter['type'] == 'text':
        <select id="operators_${filter['name']}" class="select-small" style="vertical-align: top;" onchange="toggle_operator('${filter['name']}');" name="operators[${filter['name']}]">
            <option value="~">is like</option>
            <option value="=">is</option>
            <option value="!">is not</option>
        </select>
        % elif filter['type'] == 'integer':
        <select id="operators_${filter['name']}" class="select-small" style="vertical-align: top;" onchange="toggle_operator('${filter['name']}');" name="operators[${filter['name']}]">
            <option value="=">is</option>
            <option value="&gt;">is greater than</option>
            <option value="&lt;">is less than</option>
        </select>
        % endif
        <script type="text/javascript">toggle_filter('${filter['name']}')</script>
    </td>
    <td>
        <div id="div_values_${filter['name']}" style="">
            ${h.text(id='values_'+filter['name'], name="["+filter['name']+"][]")}
        </div>
    </td>
</tr>
% endfor
</%def>
