% for i, problem in enumerate(c.problems):
<tr>
  <td class="problem_td">
    <a class="problem_info" href="${h.url(controller='nodes', action='show', id=problem['id'])}" title="${h.render_problem_info(problem)}">${problem['hostname']}</a> &ndash; <a class="problem_link problem_info" title="${h.render_problem_info(problem)}" href="${problem['a_link']}">stats</a>
    <div class="flag_list">
      <span class="problem_flag_${problem['issue']}"></span>
    </div>
  </td>
</tr>
% endfor
