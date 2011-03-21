import json
import logging
import time

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.lib.php import convert_array
from nodetraq.model.meta import Session, metadata
from nodetraq.model.nodes import Node, Group

from sqlalchemy.sql import and_

log = logging.getLogger(__name__)

class HostsController(BaseController):

    def index(self):
        func = None
        groups = None
        is_nodehash = False
        if 'groups' in request.params:
            if request.params['groups'] == 'all':
                groups = Session.query(Group).all()
            else:
                request_groups = [v for k,v in request.params.items()\
                        if 'groups' in k]
                groups = Session.query(Group)\
                        .filter(Group.name.in_(request_groups)).all()

        if groups:
            is_nodehash = True
            nodes = {}
            for g in groups:
                nodes[g.name] = [n for n in g.nodes]
        elif 'hostname' in request.params:
            response.content_type = "text/plain"
            node = Session.query(Node).filter(
                    Node.hostname == request.params['hostname'])
            if 'nagios' in request.params:
                node = node.filter(Node.nagios == request.params['nagios'])
            node = node.first()
            if node:
                return " ".join(
                    [node.primary_ip, node.hostname])
            else: return None
        else:
            nodes = Session.query(Node).all()

        if 'format' in request.params:
            func = getattr(self, 'export_' + request.params['format'])
            return func(nodes, is_nodehash)
        elif 'dump' in request.params:
            func = getattr(self, 'dump_'+request.params['dump'])
            return func(nodes, is_nodehash)
        elif 'groups' in request.params:
            func = self.show_groups
            return func(nodes, is_nodehash)
        else:
            response.content_type = "text/plain"
            c.groups = Session.query(Group).order_by('name').all()
            return render('/hosts/info.mako')

    # dump types
    @staticmethod
    def dump_machines(nodes, is_nodehash=False):
        response.content_type = "text/plain"
        dump_list = []
        for node in nodes:
            dump_list.append(
                ' '.join(
                    [node.primary_ip, node.hostname, node.server_id]))

        return '\n'.join(dump_list)

    @staticmethod
    def show_groups(groups, is_nodehash=False):
        response.content_type = "text/plain"
        c.groups = groups
        c.nagios = None
        if 'nagios' in request.params:
            if request.params['nagios']:
                c.nagios = request.params['nagios']

        for group in c.groups:
            c.groups[group].sort(key=lambda node: node.hostname)
        return render('/hosts/dumplist.mako')

    # formats
    @staticmethod
    def export_bind(nodes, is_nodehash=False):
        response.content_type = "text/plain"
        c.time = int(time.time())
        c.nodes = nodes
        c.groups = Session.query(Group).order_by('name').all()
        return render('/hosts/bind.mako')

    @staticmethod
    def export_rbind(nodes, is_nodehash=False):
        response.content_type = "text/plain"
        c.time = int(time.time())
        c.nodes = nodes
        c.groups = Session.query(Group).order_by('name').all()
        return render('/hosts/rbind.mako')

    @staticmethod
    def export_dsh(nodes, is_nodehash=False):
        response.content_type = "text/plain"
        c.groups = Session.query(Group).order_by('name').all()
        c.nodes = Session.query(Node).order_by('hostname').all()
        return render('/hosts/dsh.mako')

    @staticmethod
    def export_json(nodes, is_nodehash=False):
        response.content_type = "application/json"
        json_hash = {}
        json_hash['machines'] = []
        for node in nodes:
            json_hash['machines'].append(node.__json__())

        return json.dumps(json_hash, sort_keys=True, indent=4)

    @staticmethod
    def export_xml(nodes, is_nodehash=False):
        ignore_list = ('server_id', 'metadata')
        response.content_type = "application/xml"
        root = ET.Element("machines")

        keys = None
        for node in nodes:
            if not keys:
                keys = [v for v in dir(node) if not v.startswith('_')]
                keys = [v for v in keys if not v in ignore_list]

            machine = ET.SubElement(root, 'machine')
            for key in keys:
                elem = ET.SubElement(machine, key)
                elem.text = '%s' % getattr(node, key)

        tree = ET.ElementTree(root)
        txt = ET.tostring(root)
        return parseString(txt).toprettyxml()

    def getid(self):
        response.content_type = "text/plain"
        for key, value in request.params.iteritems():
            return str(Session.query(Node)\
                       .filter(getattr(Node, key) == \
                           value)\
                       .first().id)

    def whoami(self):
        response.content_type = "text/plain"
        if 'HTTP_X_FORWARDED_FOR' in request.environ:
            c.ip = request.environ["HTTP_X_FORWARDED_FOR"]
        if not hasattr(c, 'ip'):
            try:
                c.ip = request.environ.remote_addr
            except:
                c.ip = request.environ['REMOTE_ADDR']
        if 'mac' in request.params:
            mac = request.params['mac']
            mac = mac.replace(':', '')
            mac = mac.upper
        else: mac = None
        c.node = Session.query(Node).filter(
                Node.primary_mac == mac).first()
        return render('/nodes/whoami.mako')

    def node_from_each_pool(self):
        def get_www_groups(node, logging_group):
            groups = list(set(node.groups) - set([logging_group]))
            groups = [g for g in groups if g.name.startswith('www-')]
            return groups[0]

        response.content_type = "text/plain"
        www_groups = Session.query(Group)\
                .filter(Group.name.like('www-%')).all()
        logging_group = Session.query(Group)\
                .filter(Group.name == 'www-logging').first()
        www_groups = list(set(www_groups) - set([logging_group]))

        node_list = []
        for group in www_groups:
            found = False
            for n in sorted(group.nodes, key=lambda x: x.hostname):
                if found:
                    break
                if group in n.groups and logging_group in n.groups:
                    node_list.append(n)
                    found = True

        node_array = {}
        for n in node_list:
            n = get_www_groups(n, logging_group)

        for i,node in enumerate(node_list):
            node_array[i] = \
                {'hostname': node.hostname,
                'rack': node.rack,
                'rack_u': node.rack_u,
                'drac_ip': node.drac_ip,
                'primary_ip': node.primary_ip,
                'secondary_ip': node.secondary_ip,
                'primary_mac': node.primary_mac,
                'secondary_mac': node.secondary_mac,
                'dsh_flag': '1',
                'name': get_www_groups(node, logging_group)}

        return convert_array(node_array)

    @staticmethod
    def export_nagios_status(nodes, is_nodehash=False):
        response.content_type = "text/plain"
        c.nodes = nodes
        c.groups = Session.query(Group).order_by('name').all()
        return render('/hosts/nagios_status.mako')


