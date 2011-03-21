import logging
import datetime

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sqlalchemy.sql.expression import desc

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.model.meta import Session, now
from nodetraq.model.users import User
from nodetraq.model.activity import Activity, ActivityType

log = logging.getLogger(__name__)

class ActivityController(BaseController):

    @user_level(0)
    def __before__(self):
        super(self.__class__, self).__before__()

    def index(self, format='html'):
        c.title = 'Nodetraq - Activity'
        c.selected_page = 'activity'
        c.subpage = 'index'

        if request.params.has_key('from'):
            c.end_date = request.params['from']
            if c.end_date == now().date():
                c.last_page = True
            else:
                c.last_page = False
        else:
            c.last_page = True
            c.end_date = now().date()

        if request.params.has_key('to'):
            c.start_date = request.params['to']
        else:
            c.start_date = c.end_date - datetime.timedelta(days=3)

        if not request.params.has_key('show_nodes') and \
                not request.params.has_key('show_groups') and \
                not request.params.has_key('show_inventory'):
                    c.filters = {
                        'show_nodes': True,
                        'show_groups': True,
                        'show_inventory': True,
                        }
        else:
            c.filters = {
                    'show_nodes': False,
                    'show_groups': False,
                    'show_inventory': False,
                    }

        for key in c.filters.keys():
            if request.params.has_key(key):
                c.filters[key] = request.params[key]

        # add filters to be checked by sqlalchemy
        filters = []
        for k in c.filters:
            if c.filters[k]:
                if k[5:] == 'groups' or k[5:] == 'nodes':
                    filters.append(k[5:-1])
                else:
                    filters.append(k[5:])

        if filters:
            activity_types = Session.query(ActivityType)\
                    .filter(
                        ActivityType.name.in_(filters)).all()
            activity_type_ids = [a_type.id for a_type in activity_types]
            c.activities = Activity.get_activity_page()
            '''
            c.activities = Session.query(Activity)\
                    .filter(
                        Activity.activity_type_id.in_(activity_type_ids))\
                                .order_by(desc(Activity.created_at))\
                                .filter(Activity.parent == None).all()
            '''
        else:
            c.activities = Activity.get_activity_page()

        if format == 'html':
            return render('/activity/index.mako')
        elif format == 'json':
            response.content_type = "application/json"
            return render('/activity/index.json')
        elif format == 'xml':
            response.content_type = "application/xml"
            return render('/activity/index.xml')

    def info(self, id):
        c.title = 'Nodetraq - Activity - Info'
        c.selected_page = 'activity'
        c.subpage = 'info'

        c.activity = Session.query(Activity)\
                .filter(Activity.id == id).first()
        c.Session = Session
        return render('/activity/info.mako')

    def atom(self):
        yesterday = now()- datetime.timedelta(hours=18)
        c.activity = Session.query(Activity)\
                .filter(Activity.created_at < now())\
                .filter(Activity.created_at > yesterday)\
                .order_by(desc(Activity.created_at))\
                .filter(Activity.parent == None)\
                .all()
        return render('/activity/atom.mako')

