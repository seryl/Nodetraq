import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node
from nodetraq.lib.activity import ActivityEngine

log = logging.getLogger(__name__)

class PuppetController(BaseController):

    def status(self, hostname):
        response.content_type = "text/plain"
        if not hostname:
            return "False"
        node = Session.query(Node)\
            .filter(Node.hostname == hostname).first()
        if node:
            return '%s' % node.puppet

    def addpuppet(self):
        response.content_type = "application/json"
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        else:
            session['flash'] = 'No ids were sent'
            session.save()
            return '{"success": false}'

        data = {}
        data['add_puppet'] = True

        activity_engine = ActivityEngine(
            Session, session['active_user']['user_id'])
        status = activity_engine.update_many('group', ids, data)

        session['flash'] = status
        session.save()
        return '{"success": true}'

    def removepuppet(self):
        response.content_type = "application/json"
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        else:
            session['flash'] = 'No ids were sent'
            session.save()
            return '{"success": false}'

        data = {}
        data['remove_puppet'] = True

        activity_engine = ActivityEngine(
            Session, session['active_user']['user_id'])
        status = activity_engine.update_many('group', ids, data)

        session['flash'] = status
        session.save()
        return '{"success": true}'

