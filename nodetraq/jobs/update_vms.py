#!/usr/local/bin/python2.6
from paste.deploy import appconfig
from pylons import config

from sqlalchemy.sql import and_

from nodetraq.config.environment import load_environment
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node, Group
from nodetraq.lib.sshwrapper import run_ssh_command

conf = appconfig('config:production.ini', relative_to='../../')
load_environment(conf.global_conf, conf.local_conf)

class XenInfo(object):
    def __init__(self):
        self.hostname = ''
        self.id = 0
        self.mem = 0
        self.vcpus = 0
        self.state = "------"
        self.time = 0
        self.location = 'sv2'
        self.rack = 0
        self.rack_u = 0

def get_xen_list(xen_group):
    # Aggregate xen-dom0 info
    xeninfo = []
    for node in xen_group.nodes:
        # Get listing of nodes
        xen_data = run_ssh_command('root@' + node.hostname, 'xm list')
        # Split based on newline
        xen_data = xen_data[0].split('\n')[2:]
        # For each line; create a xen info item
        for line in xen_data:
            line = line.split()
            if line:
                xen = XenInfo()
                xen.hostname = line[0]
                xen.id = int(line[1])
                xen.mem = int(line[2])
                xen.vcpus = int(line[3])
                xen.state = line[4]
                xen.time = line[5]

                xen.location = node.location
                xen.rack = node.rack
                xen.rack_u = node.rack_u

            xeninfo.append(xen)

    return xeninfo

def update_xen_nodes(xen_list):
    for item in xen_list:
        node = Session.query(Node).filter(
            Node.hostname == item.hostname).first()
        if not node:
            node = Node()
            node.hostname = item.hostname
            node.memory = item.mem

        node.xen_instance = item.id
        node.location = item.location
        node.rack = item.rack
        node.rack_u = item.rack_u

        Session.add(node)
    Session.commit()
    return True

def update_vms():
    xen_group = Session.query(Group)\
        .filter(Group.name == 'xen-dom0').first()
    vm_group = Session.query(Group)\
        .filter(Group.name == 'vm').first()
    vm_hosts = xen_group.nodes

    update_xen_nodes(get_xen_list(xen_group))

    for node in Session.query(Node).all():
        if node.xen_instance:
            if not vm_group in node.groups:
                node.groups.append(vm_group)

    for host in vm_hosts:
        vm_instances = Session.query(Node)\
            .filter(and_(Node.rack == host.rack,
                    Node.rack_u == host.rack_u,
                    )).all()
        vm_instances = [v for v in vm_instances if v not in vm_hosts]

        for node in vm_instances:
            n = Session.query(Node).filter(
                    Node.hostname == node.hostname).first()
            n.service_tag = host.service_tag
            n.drac_ip = None
            Session.add(n)
            Session.commit()

if __name__ == '__main__':
    update_vms()
