import logging
from urllib import urlencode

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators.cache import beaker_cache

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.lib.F5 import LoadBalancer
from nodetraq.lib.activity import ActivityEngine
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node

from sqlalchemy import or_

log = logging.getLogger(__name__)

class LoadbalancerController(BaseController):

    @user_level(0)
    def __before__(self):
        super(self.__class__, self).__before__()

    def index(self):
        c.title = 'Nodetraq - LoadBalancer'
        c.selected_page = 'loadbalancer'
        c.subpage = 'index'
        lb = LoadBalancer(ip='lb_iphere')
        pools = lb.get_pools()
        pools.sort()
        c.pool_count = len(pools)

        c.link_append = '&' + urlencode(
            [p for p in request.params.items()\
                 if p[0] != 'page'])
        if c.link_append == '&':
            c.link_append = None

        if 'show_all' in request.params:
            c.page = 1
            c.total_pages = 1
            c.current_page_count = 1
            c.members = self.get_members_status(Session, pools)
        else:
            c.page = int(request.params['page'])\
                    if 'page' in request.params else 1
            c.total_pages = (c.pool_count+25-1)/25
            c.current_page_count = (c.page-1)*25
            c.members = self.get_members_status(Session,
                    pools[c.current_page_count:c.current_page_count+25])

        return render('/loadbalancer/index.mako')

    def create(self):
        c.title = 'Nodetraq - Loadbalancer - Create Pool'
        c.selected_page = 'loadbalancer'
        c.subpage = 'create'
        return render('/loadbalancer/create.mako')

    def show(self, pool):
        c.title = 'Nodetraq - Loadbalancer - Show'
        c.selected_page = 'loadbalancer'
        c.subpage = 'show'
        lb = LoadBalancer(ip='your_lb_ip')
        c.members = self.get_members_status(Session, [pool])[0]
        return render('/loadbalancer/show.mako')

    def newcomment(self):
        c.title = 'Nodetraq - Loadbalancer - Create Comment'
        c.selected_page = 'loadbalancer'
        c.subpage = 'comment'
        c.user_id = session['active_user']['user_id']
        return render('/loadbalancer/comments/new.mako')

    def createcomment(self, pool):
        if 'comment' in request.params and\
                'user_id' in request.params:
            if request.params['comment']:
                lbcomment = LBPoolComments()
                lbcomment.comment =request.params['comment']
                if request.params['user_id']:
                    lbcomment.user_id = request.params['user_id']
                Session.add(lbcomment)
                Session.commit()
            else:
                session['flash'] = 'Creating comment failed'
                session.save()

        return redirect(url(
            controller='loadbalancer', action='show',
            pool=c.request.params['pool']))

    def createpool(self, format=None):
        response.content_type = "application/json"
        has_members = False
        ids = None
        ips = None
        use_primary = True

        if 'pool' in request.params:
            pool = request.params['pool']
        else:
            session['flash'] = 'Pool was not created'
            session.save()
            if format == 'json':
                return '{"success": false}'
            else:
                return redirect(url(
                        controller='loadbalancer', action='index'))

        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
            if 'use_secondary' in request.params:
                use_primary = False
        if 'ips[]' in request.params:
            ips = [v for k,v in request.params.items() if 'ips[]' in k]
        if ips or ids:
            if 'port' in request.params:
                port = request.params['port']
                has_members = True
        else:
            ids,ips,port = None,None,None

        lb = LoadBalancer(ip='your_lb_ip')
        mem_seq = lb.b.LocalLB.Pool.typefactory.create(
                'Common.IPPortDefinitionSequence')
        if ids:
            if use_primary:
                mem_seq.item = [lb._member_factory(
                    ':'.join([Session.query(Node.primary_ip)\
                            .filter(Node.id == id)\
                            .first()[0], port])) for id in ids]
            else:
                mem_seq.item = [lb._member_factory(
                    ':'.join([Session.query(Node.secondary_ip)\
                            .filter(Node.id == id)\
                            .first()[0], port])) for id in ids]
        elif ips:
            mem_seq.item = [lb._member_factory(
                ':'.join([ip, port])) for ip in ips]

        if not has_members:
            mem_seq = []

        lb.create_pool(pool, mem_seq)
        data = {}
        data['pool'] = pool
        if ids:
            data['hosts'] = [
                Session.query(Node)\
                    .filter(Node.id == id).first()\
                    for id in ids ]
        if ips:
            data['hosts'] = [
                Session.query(Node)\
                    .filter(or_(Node.primary_ip.in_([ips]),
                                Node.secondary_ip.in_([ips])))\
                    .first() for id in ids ]
        ae = ActivityEngine(
            Session, session['active_user']['user_id'])

        status = ae.create('loadbalancer', data)
        session['flash'] = status
        session.save()
        if format == 'json':
            return '{"success": true}'
        else:
            return redirect(url(
                    controller='loadbalancer', action='index'))

    def deletepool(self, format=None):
        if 'pools[]' in request.params:
            pool = [v for k,v in request.params.items() if 'pools[]' in k]
        else:
            return '{"success": false}'

        lb = LoadBalancer(ip='your_lb_ip')
        lb.delete_pool(pool)
        data = {}
        data['pools'] = pool
        ae = ActivityEngine(
            Session, session['active_user']['user_id'])

        status = ae.destroy('loadbalancer', data)
        session['flash'] = status
        session.save()
        if format == 'json':
            return '{"success": true}'
        else:
            return redirect(url(
                    controller='loadbalancer', action='index'))

    def enablehost(self, format=None):
        valid = False
        response.content_type = "application/json"
        ids = None
        ips = None
        data = {}
        ports = []
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        elif 'ips[]' in request.params:
            ips = [v for k,v in request.params.items() if 'ips[]' in k]
        if 'pool' in request.params:
            pool = request.params['pool']
            if 'ports[]' in request.params:
                ports = [v for k,v in request.params.items()\
                        if 'ports[]' in k]
                if ips or ids:
                    valid = True

        if not valid:
            session['flash'] = 'No ids were sent'
            session.save()
            if format == 'json':
                return '{"success": false}'
            else:
                return redirect(url(
                        controller='loadbalancer', action='index'))

        lb = LoadBalancer(ip='your_lb_ip')
        if ids:
            data['hosts'] = [
                Session.query(Node.hostname)\
                    .filter(Node.id == id)\
                    .first()[0] for id in ids ]
            members = [
                    ':'.join([Session.query(Node.primary_ip)\
                        .filter(Node.id == id)\
                        .first()[0], ports[i]])\
                        for i,id in enumerate(ids)]
        elif ips:
            data['hosts'] = [
                Session.query(Node.hostname)\
                    .filter(or_(Node.primary_ip == ip,
                                Node.secondary_ip == ip))\
                    .first()[0] for ip in ips ]
            members = [':'.join([ip, ports[i]])\
                    for i,ip in enumerate(ips)]

        lb.enable_members(pool, members)
        data['pool'] = pool
        data['type'] = 'enable'
        ae = ActivityEngine(
            Session, session['active_user']['user_id'])

        status = ae.update('loadbalancer', None, data)
        session['flash'] = status
        session.save()
        if format == 'json':
            return '{"success": true}'
        else:
            return redirect(url(
                    controller='loadbalancer', action='index'))

    def disablehost(self, format=None):
        valid = False
        response.content_type = "application/json"
        ids = None
        ips = None
        data = {}
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        elif 'ips[]' in request.params:
            ips = [v for k,v in reuqest.params.items() if 'ips[]' in k]
        if 'pool' in request.params:
            pool = request.params['pool']
            if 'ports[]' in request.params:
                ports = [v for k,v in request.params.items()\
                        if 'ports[]' in k]
                if ids or ips:
                    valid = True

        if not valid:
            session['flash'] = 'No ids were sent'
            session.save()
            if format == 'json':
                return '{"success": false}'
            else:
                return redirect(url(
                        controller='loadbalancer', action='index'))

        lb = LoadBalancer(ip='your_lb_ip')
        if ids:
            data['hosts'] = [ q[0] for q in\
                    Session.query(Node.hostname)\
                .filter(Node.id.in_(ids)).all() ]
            members = [
                ':'.join([Session.query(Node.primary_ip)\
                        .filter(Node.id == id)\
                        .first()[0], ports[i]])\
                    for i,id in enumerate(ids)]
        elif ips:
            data['hosts'] = [q[0] for q in Session.query(Node.hostname)\
                .filter(or_(Node.primary_ip.in_(ips),
                            Node.secondary_ip.in_(ips)))\
                            .all() ]
            members = [
                ':'.join([ip, ports[i]]) for i,ip in enumerate(ips)]

        lb.disable_members(pool, members)
        data['type'] = 'disable'
        data['pool'] = pool
        ae = ActivityEngine(
            Session, session['active_user']['user_id'])

        status = ae.update('loadbalancer', None, data)
        session['flash'] = status
        if format == 'json':
            return '{"success": true}'
        else:
            return redirect(url(
                    controller='loadbalancer', action='index'))

    def addhost(self, format=None):
        valid = False
        response.content_type = "application/json"
        ids = []
        ips = []
        ports = []
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        if 'ips[]' in request.params:
            ips = [v for k,v in request.params.items() if 'ips[]' in k]
        if 'pool' in request.params:
            pool = request.params['pool']
            if 'ports[]' in request.params:
                ports = [v for k,v in request.params.items()\
                        if 'ports[]' in k]
        if ids or ips:
            if ports:
                valid = True

        if not valid:
            session['flash'] = 'No ids were sent'
            session.save()
            if format == 'json':
                return '{"success": false}'
            else:
                return redirect(url(
                        controller='loadbalancer', action='index'))

        lb = LoadBalancer(ip='your_lb_ip')
        members = lb.b.LocalLB.Pool.typefactory.create(
                'Common.IPPortDefinitionSequence')

        data = {}
        if ids:
            data['hosts'] = [
                Session.query(Node.hostname)\
                    .filter(Node.id == id)\
                    .first()[0] for id in ids ]
            iplist = [ip[0] for ip in Session.query(Node.primary_ip)\
                .filter(Node.id.in_(ids)).all()]

            members.item = [lb._member_factory(
                ':'.join([ip, ports[i]]))\
                                for i,ip in enumerate(iplist)]
        if ips:
            data['hosts'] = [ q[0] for q in\
                Session.query(Node.hostname)\
                    .filter(or_(Node.primary_ip == ip,
                                Node.secondary_ip == ip))\
                    .all() for ip in ips ]
            members.item = [lb._member_factory(
                ':'.join([ip, port]))\
                                for i,ip in enumerate(ips)]

        lb.add_members(pool, members)
        data['pool'] = pool
        data['type'] = 'add'
        ae = ActivityEngine(
            Session, session['active_user']['user_id'])
        if len(ids) > 2 or len(ips) > 2:
            status = ae.update_many('loadbalancer', data)
        else:
            status = ae.update('loadbalancer', None, data)
        session['flash'] = status
        session.save()
        if format == 'json':
            return '{"success": true}'
        else:
            return redirect(url(
                    controller='loadbalancer', action='index'))

    def removehost(self, format=None):
        valid = False
        response.content_type = "application/json"
        ids = []
        ips = []
        data = {}
        ports = []
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        if 'ips[]' in request.params:
            ips = [v for k,v in request.params.items() if 'ips[]' in k]
        if 'pool' in request.params:
            pool = request.params['pool']
            if 'ports[]' in request.params:
                ports = [v for k,v in request.params.items()\
                        if 'ports[]' in k]
        if ids or ips:
            if ports:
                valid = True

        if not valid:
            session['flash'] = 'No ids were sent'
            session.save()
            if format == 'json':
                return '{"success": false}'
            else:
                return redirect(url(
                        controller='loadbalancer', action='index'))
        lb = LoadBalancer(ip='your_lb_ip')
        members = lb.b.LocalLB.Pool.typefactory.create(
                'Common.IPPortDefinitionSequence')

        if ids:
            data['hosts'] = [
                q[0] for q in\
                    Session.query(Node.hostname)\
                    .filter(Node.id.in_(ids)).all() ]

            members.item = [lb._member_factory(
                ':'.join([Session.query(Node.primary_ip)\
                        .filter(Node.id == id).first()[0],
                        ports[i]])) for i,id in enumerate(ids)]
        if ips:
            data['hosts'] = [ q[0] for q in \
                    Session.query(Node.hostname)\
                    .filter(or_(Node.primary_ip.in_(ips),
                            Node.secondary_ip.in_(ips)))\
                            .all() ]
            members.item = [lb._member_factory(
                ':'.join(ip, ports[i])) for i,ip in enumerate(ips)]

        lb.remove_members(pool, members)
        data['type'] = 'remove'
        data['pool'] = pool
        ae = ActivityEngine(
            Session, session['active_user']['user_id'])
        status = ae.update('loadbalancer', None, data)
        session['flash'] = status
        session.save()
        if format == 'json':

            return '{"success": true}'
        else:
            return redirect(url(
                    controller='loadbalancer', action='index'))

    @staticmethod
    def get_members_status(Session, pools):
        lb = LoadBalancer(ip='your_lb_ip')
        pool_members = lb.get_member_status(pools)
        for x,pool in enumerate(pool_members):
            for y,member in enumerate(pool):
                node = Session.query(Node)\
                        .filter(or_(
                            Node.primary_ip == member['member']['address'],
                            Node.secondary_ip == member['member']['address']))\
                                    .first()
                if member.session_state == "STATE_ENABLED":
                    member.session_state = True
                else:
                    member.session_state = False
                pool_members[x][y] = (node, member['member']['port'], member.session_state)

        return zip(pools, pool_members)

