"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.tags import *
from webhelpers.markdown import markdown
from pylons import url

from nodetraq.model.meta import now
from gravatar import gravatar
from util.network import str_to_mac, rbind
from sort_nodes import generate_sort
from dashboard import render_sync_issue, render_flag_info, render_problem_info
from drraw import alphaenum
from nagios import nagios_current_time
from urllib import quote
