Load Balancer:
<select id="selected_group" name="selected_group">
    % for lb in c.loadbalancers:
    <option value="${lb}">${lb}</option>
    % endfor
</select>

