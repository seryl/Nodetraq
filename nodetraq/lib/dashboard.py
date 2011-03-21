def render_sync_issue(sync_issues):
    text = 'type : value : reported<br /><br />'
    for issues in sync_issues['issues']:
        text += ' : '.join([str(issues['type']),
                   str(issues['value']),
                   str(issues['reported'])])
        text += '<br />'

    return text

def render_flag_info(info):
    text = 'Flags:<br />'
    text += '<div style="margin-left: 12px;">'
    text += '<br />'.join(
        [f.name for f in info.flags])
    text += '</div>'
    return text

def render_problem_info(problem):
    text = 'Stats:<br />'
    text += '<div style="margin-left: 12px;">'
    for k in ['pool', 'data_age', 'httpd_reqs',
            'httpd_idle','httpd_act', 'load1',
            'load5', 'load15', 'memfreepercent',
            'memtotal_kb']:
        text += ' : '.join([k, str(problem[k])])
        text += '<br />'
    text += '</div>'
    return text

