#!/usr/local/bin/python2.6
from paste.deploy import appconfig
from pylons import config

from nodetraq.config.environment import load_environment
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node, Group

import re

conf = appconfig('config:production.ini', relative_to='../../')
load_environment(conf.global_conf, conf.local_conf)

def create_group(name):
    group = Group()
    group.name = name
    Session.add(group)
    Session.commit()
    return group

def update_groups():
    regex = '^r\d{3}$'
    for node in Session.query(Node).all():
        rack_name = 'r%s' % node.rack

        # create the group if it doesn't exist
        group = Session.query(Group)\
           .filter(Group.name == rack_name).first()

        if not group:
           group = create_group(rack_name)

        # add that computer to the group
        node.groups.append(group)
        Session.add(node)
        Session.commit()

        # Remove rack groups that a node is no longer a part of
        found_groups = [g for g in node.groups\
                            if re.search(regex, g.name) and g != group]

        for bad_group in found_groups:
            node.groups.remove(bad_group)

        Session.add(node)
        Session.commit()

if __name__ == '__main__':
    update_groups()

