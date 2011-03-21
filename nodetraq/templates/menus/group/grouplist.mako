Group: 
<select id="selected_group" name="selected_group">
    % for group in c.groups:
    <option value="${group[0]}">${group[0]}</option>
    % endfor
</select>

