import logging
import urllib
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.model.meta import Session
from nodetraq.model.nodes import Node
from nodetraq.model.dashboard import NodeFlagInfo

from sqlalchemy.sql.expression import asc

log = logging.getLogger(__name__)

class DashboardController(BaseController):

    @user_level(0)
    def __before__(self):
        super(self.__class__, self).__before__()

    def index(self):
        c.title = 'Nodetraq - Dashboard'
        c.selected_page = 'dashboard'
        c.subpage = 'index'

        c.sync_issues = self.get_sync_issues()['issues']
        return render('/dashboard/index.mako')

    def atom(self):
        return render('/dashboard/atom.mako')

    def get_sync_issues(self):
        nodes = Session.query(Node).order_by(
            asc('hostname')).all()
        sync_issues = {'issues': []}
        for node in nodes:
            if node.sync_issues:
                sync_issues['issues'].append({
                        'id': node.id,
                        'hostname': node.hostname,
                        'issues': node.sync_issues})
        return sync_issues

    def get_problems(self):
        aq_mon = 'amqp_server_here'
        aq_link = 'amqp_base_link'
        problems = json.loads(urllib.urlopen(aq_mon).read())
        for problem in problems['issues']:
            problem['a_link'] = aq_link + problem['pool'] + \
                    '#' + problem['hostname']
            problem['id'] = Session.query(Node.id).filter(
                    Node.hostname == problem['hostname']).first()[0]

        ordered_problems = []
        for problem in problems['issues']:
            if problem['issue'] == 'problem':
                ordered_problems.append(problem)
        for problem in problems['issues']:
            if problem['issue'] == 'warning':
                ordered_problems.append(problem)
        for problem in problems['issues']:
            if problem['issue'] == 'timeout':
                ordered_problems.append(problem)

        return ordered_problems

    def display_problems(self):
        c.problems = self.get_problems()
        return render('/dashboard/display_problems.mako')

    def display_flags(self):
        c.node_flag_info = Session.query(NodeFlagInfo).all()
        return render('/dashboard/display_flags.mako')

