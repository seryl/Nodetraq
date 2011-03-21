#!/usr/local/bin/python2.6
from paste.deploy import appconfig
from pylons import config

from nodetraq.config.environment import load_environment
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node, Group

import re
import string

conf = appconfig('config:production.ini', relative_to='../../')
load_environment(conf.global_conf, conf.local_conf)

def create_group(name):
    group = Group()
    group.name = name
    Session.add(group)
    Session.commit()
    return group


def generate_groupname(model_name):
    if not model_name:
        return None
    if model_name in ['DELL', '1']:
        return None
    model_group, model_class = model_name.split()
    model_group = ''.join(
            [c for c in model_group \
                    if c in string.ascii_uppercase])
    return '-'.join([model_group, model_class.upper()])


def update_groups():
    for node in Session.query(Node)\
            .filter(Node.model_name != None).all():

        # create the group if it doesn't exist
        group = Session.query(Group)\
           .filter(Group.name == generate_groupname(node.model_name)).first()

        if not group:
           group = create_group(generate_groupname(node.model_name))

        # add that computer to the group
        if not group in node.groups:
            node.groups.append(group)
            Session.add(node)
            Session.commit()

            # Remove rack groups that a node is no longer a part of
            # found_groups = [g for g in node.groups\
            #                    if re.search(regex, g.name) and g != group]

            # for bad_group in found_groups:
            #    node.groups.remove(bad_group)

            Session.add(node)
            Session.commit()


if __name__ == '__main__':
    update_groups()

