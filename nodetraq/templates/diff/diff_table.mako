<table>
  <thead>
  </thead>
  <tbody>
    <tr>
      <td>
        % for line in c.diff.split('\n'):
        % if line.startswith('- '):
        <span class="diff_removed">${line}</span><br />
        % elif line.startswith('+ '):
        <span class="diff_added">${line}</span><br />
        % else:
        ${line}<br />
        % endif
        % endfor
      </td>
    </tr>
  </tbody>
</table>
