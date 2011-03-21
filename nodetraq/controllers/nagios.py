import logging
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from nodetraq.lib.base import BaseController, render
from nodetraq.model.meta import Session
from nodetraq.model.nodes import Node
from nodetraq.lib.nagios import schedule_host_downtime,\
    enable_host_service_notifications, disable_host_service_notifications,\
    acknowledge_svc_problem, acknowledge_host_problem,\
    remove_nagios_monitors, remove_from_downtime
log = logging.getLogger(__name__)

class NagiosController(BaseController):

    def schedule_downtime(self):
        return render('/nodes/nagios/schedule_downtime.mako')

    @jsonify
    def schedule_host_downtime(self):
        data = None
        for k,v in request.params.iteritems():
            if isinstance(k, str):
                data = json.loads(k)
                data = data['data']
                break

        nodes = Session.query(Node).filter(
            Node.id.in_(data['ids'])).all()

        for node in nodes:
            schedule_host_downtime(
                node.hostname, data['start_time'],
                data['end_time'], author=data['author'],
                comment=data['comment'])
        session['flash'] = 'Successfully scheduled downtime'
        session.save()
        return str({'params': request.params})

    @jsonify
    def enable_host_svc(self):
        id_list = []
        hostname_list = []
        for k,v in request.params.iteritems():
            if k == 'ids[]':
                id_list.append(int(v))
            if k == 'hostname':
                hostname_list.append(v)

        if id_list:
            nodes = Session.query(Node.hostname).filter(
                Node.id.in_(id_list)).all()
            for node in nodes:
                enable_host_service_notifications(node[0])
            session['flash'] = 'Enabled host services successfully'
            session.save()
            return str({'success': True})
        elif hostname_list:
            nodes = Session.query(Node.hostname).filter(
                Node.hostname.in_(hostname_list)).all()
            for node in nodes:
                enable_host_service_notifications(node[0])
            session['flash'] = 'Enabled host services successfully'
            session.save()
            return str({'success': True})
        else:
            session['flash'] = 'Enable host services failed'
            session.save()
            return str({'success': False})

    @jsonify
    def disable_host_svc(self):
        id_list = []
        for k,v in request.params.iteritems():
            if k == 'ids[]':
                id_list.append(int(v))

        if id_list:
            nodes = Session.query(Node.hostname).filter(
                Node.id.in_(id_list)).all()
            for node in nodes:
                disable_host_service_notifications(node[0])
                session['flash'] = 'Disabled host services successfully'
                session.save()
            return str({'success': True})
        else:
            session['flash'] = 'Disabled host services successfully'
            session.save()
            return {'success': False}

    @jsonify
    def remove_nagios_monitors(self):
        id_list = []
        for k,v in request.params.iteritems():
            if k == 'ids[]':
                id_list.append(int(v))

        for node_id in id_list:
            node = Session.query(Node).filter(Node.id == node_id).first()
            remove_nagios_monitors(node.hostname)

        return {'success': True}

    @jsonify
    def acknowledge_svc_problem(self, hostname=None):
        service=request.params["service"]
        if not hostname:
            return {'success': False}
        if not service:
            return {'success': False}
        acknowledge_svc_problem(hostname, service)
        return str({'success': True})

    @jsonify
    def acknowledge_host_problem(self, hostname=None):
        if not hostname:
            return {'success': False}
        acknowledge_host_problem(hostname)
        return str({'success': True})

    @jsonify
    def remove_from_downtime(self):
        id_list = []
        for k,v in request.params.iteritems():
            if k == 'ids[]':
                id_list.append(int(v))
        try:
            for node_id in id_list:
                node = Session.query(Node).filter(Node.id == node_id).first()
                remove_from_downtime(node.hostname)
            return {'success': True}
        except:
            return {'success': False}

