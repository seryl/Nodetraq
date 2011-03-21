import logging

from operator import attrgetter

from urllib import urlencode

from pylons import request, response, session, tmpl_context as c, url
from pylons.decorators.cache import beaker_cache
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.model.meta import Session, metadata
from nodetraq.model.nodes import Group, Node
from nodetraq.lib.activity import ActivityEngine
from nodetraq.lib.util.tag import get_tag_sizes
from nodetraq.lib.query import get_fields_and_query

log = logging.getLogger(__name__)

class GroupsController(BaseController):

    @user_level(0)
    def __before__(self):
        super(self.__class__, self).__before__()
        c.all_groups = None

    def index(self):
        c.page = int(request.params['page'])\
                if 'page' in request.params else 1
        c.title = 'Nodetraq - Groups'
        c.selected_page = 'groups'
        c.subpage = 'list'
        c.heading = "Groups"
        c.filters = [
                { 'name': 'group', 'label': 'Group', 'type': 'text' }
            ]
        query, c.search_fields = get_fields_and_query(Session,
                Group, request.params)
        c.request_url = request.environ.get('PATH_INFO')
        if request.environ.get('QUERY_STRING'):
            c.request_url += '?' + request.environ['QUERY_STRING']
        c.group_count = query.count()

        c.link_append = '&' + urlencode(\
                [p for p in request.params.items()\
                    if p[0] != 'page'])
        if c.link_append == '&':
            c.link_append = None

        if 'show_all' in request.params:
            c.total_pages = 1
            c.current_page_count = 1
            c.groups = query.order_by('name').all()
        else:
            c.total_pages = (c.group_count+25-1)/25
            c.current_page_count = (c.page-1)*25
            c.groups = query.order_by('name')\
                    [c.current_page_count: c.current_page_count+25]

        c.all_groups, c.tag_sizes = self.get_tag_info()
        return render('/groups/list.mako')

    def edit(self, id):
        id = unicode(id)
        if id.isdigit():
            c.group = Session.query(Group).filter(Group.id == id).first()
        else:
            c.group = Session.query(Group).filter(Group.name == id).first()
        c.title = 'Nodetraq - Edit group %s' % c.group.name
        c.selected_page = 'groups'
        c.subpage = 'edit'

        return render('/groups/edit.mako')

    def new(self):
        c.title = 'Nodetraq - New group'
        c.selected_page = 'groups'
        c.subpage = 'new'

        return render('/groups/new.mako')

    def create(self):
        data = {}

        data['name'] = request.params['name']
        data['description'] = request.params['description']

        activity_engine = ActivityEngine(Session,
                session['active_user']['user_id'])
        status = activity_engine.create('group', data)

        if status:
            session['flash'] = status
            session.save()

        return redirect(url(controller='groups', action='index'))

    def show(self, id, format='html'):
        id = unicode(id)
        if id.isdigit():
            c.group = Session.query(Group).filter(Group.id == int(id)).first()
        else:
            c.group = Session.query(Group).filter(Group.name == id).first()
        c.group_list = [g[0] for g in Session.query(Group.name)]

        c.title = 'Nodetraq - Group - %s' % c.group.name
        c.selected_page = 'groups'
        c.subpage = 'show'
        c.header = 'Groups : %s' % c.group.name
        c.page = int(request.params['page'])\
                if 'page' in request.params else 1
        c.current_page_count = (c.page-1) * 25
        c.node_count = len(c.group.nodes)
        c.filters = [
            { 'name': 'group', 'label': 'Group', 'type': 'text' }
            ]
        c.link_append = None
        is_sorted = False

        if 'sort' in request.params:
            sortkey, sortorder = request.params['sort'].split(':')
            is_sorted = True
            c.sort_order = sortorder
        else:
            c.sort_order = None

        if is_sorted:
            if sortorder == 'asc':
                c.nodes = c.group.nodes\
                    [c.current_page_count:c.current_page_count+25]
                c.nodes = sorted(c.nodes, key=attrgetter(sortkey), reverse=False)
            else:
                c.nodes = c.group.nodes\
                    [c.current_page_count:c.current_page_count+25]
                c.nodes = sorted(c.nodes, key=attrgetter(sortkey), reverse=True)
        else:
            c.nodes = c.group.nodes[c.current_page_count:c.current_page_count+25]
        c.all_groups, c.tag_sizes = self.get_tag_info()
        c.total_pages = (c.node_count+25-1)/25

        c.request_url = request.environ.get('PATH_INFO')
        if request.environ.get('QUERY_STRING'):
            c.request_url += '?' + request.environ['QUERY_STRING']

        if format == 'html':
            return render('/nodes/list.mako')
        elif format == 'json':
            return c.group.__json__()
        elif format == 'xml':
            return c.group.__xml__()

    def update(self):
        id = request.params['group_id']
        data = {}
        data['name'] = request.params['name']
        data['description'] = request.params['description']

        activity_engine = ActivityEngine(Session,
                session['active_user']['user_id'])
        status = activity_engine.update('group', id, data)
        session['flash'] = status
        session.save()
        return redirect(url(controller='groups', action='index'))

    def add(self):
        c.group = Session.query(Group).filter(Group.id == id).first()
        c.title = 'Nodetraq - Group - Add'
        c.selected_page = 'groups'
        c.subpage = 'add'

        return render('/groups/add.mako')

    def destroy(self, id):
        activity_engine = ActivityEngine(Session,
                session['active_user']['user_id'])
        status = activity_engine.destroy('group', id)
        session['flash'] = status
        session.save()
        return redirect(url(controller='groups', action='index'))

    @staticmethod
    @beaker_cache(expire=300)
    def get_tag_info():
        groups = Session.query(Group).order_by('name').all()
        tag_sizes = get_tag_sizes('group', groups)
        return (groups, tag_sizes)

