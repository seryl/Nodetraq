#!/usr/local/bin/python2.6
from paste.deploy import appconfig
from pylons import config

from nodetraq.config.environment import load_environment
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node, Group

from sqlalchemy import not_

conf = appconfig('config:production.ini', relative_to='../../')
load_environment(conf.global_conf, conf.local_conf)

def create_group(name):
    group = Group()
    group.name = name
    Session.add(group)
    Session.commit()
    return group

def update_groups():
    for node in Session.query(Node)\
        .filter(Node.hostname.startswith('sv')).all():

        # create the group if it doesn't exist
        group = Session.query(Group)\
           .filter(Group.name == 'idle').first()

        if not group:
           group = create_group('idle')

        # add that computer to the group
        node.groups = []
        node.groups.append(group)
        Session.add(node)
        Session.commit()

    for group in Session.query(Group)\
            .filter(Group.name == 'idle')\
            .all():
        if group:
            for node in group.nodes:
                if not node.hostname.startswith('sv'):
                    group.nodes.remove(node)

        Session.commit()

if __name__ == '__main__':
    update_groups()

