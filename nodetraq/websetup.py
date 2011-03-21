"""Setup the nodetraq application"""
import json
import logging
import os

import pylons.test

from nodetraq.config.environment import load_environment
from nodetraq.model.meta import Session, metadata, Base
from nodetraq.model.users import User
from nodetraq.model.activity import Activity, ActivityType, Changeset
from nodetraq.model.nodes import Node, Group, NodeDatabaseBackup, BackupType
from nodetraq.model.dashboard import Flag, NodeFlagInfo
from nodetraq.model.graphs import Graph
from nodetraq.lib.drraw import rrd_types
from nodetraq.lib.activity import ActivityEngine
from nodetraq.lib.util.csv_import import node_csv_import, node_csv2json

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup nodetraq here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)
    # Use the below only if you're not using declarative.
    # metadata.create_all(bind=Session.bind)

    # Setup the Activity Types
    a_type = ActivityType()
    a_type.name = 'node'
    a_type.action = 'add'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'node'
    a_type.action = 'remove'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'node'
    a_type.action = 'update'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'group'
    a_type.action = 'add'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'group'
    a_type.action = 'remove'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'group'
    a_type.action = 'update'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'inventory'
    a_type.action = 'add'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'inventory'
    a_type.action = 'remove'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'inventory'
    a_type.action = 'update'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'loadbalancer'
    a_type.action = 'add'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'loadbalancer'
    a_type.action = 'remove'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'loadbalancer'
    a_type.action = 'update'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'nagios'
    a_type.action = 'enable'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'puppet'
    a_type.action = 'enable'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'puppet'
    a_type.action = 'disable'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'user'
    a_type.action = 'create'
    Session.add(a_type)

    a_type = ActivityType()
    a_type.name = 'user'
    a_type.action = 'update'
    Session.add(a_type)

    # Setup Flags
    flag = Flag()
    flag.name = 'setup'
    flag.description = ''
    Session.add(flag)

    flag = Flag()
    flag.name = 'hardware'
    flag.description = ''
    Session.add(flag)

    flag = Flag()
    flag.name = 'maintenance'
    flag.description = ''
    Session.add(flag)

    flag = Flag()
    flag.name = 'rebooting'
    flag.description = ''
    Session.add(flag)

    flag = Flag()
    flag.name = 'examining'
    Session.add(flag)
    Session.commit()

    backup = BackupType()
    backup.name = 'xtrabackup'
    Session.add(backup)
    Session.commit()

    backup = BackupType()
    backup.name = 'one-off-backup'
    Session.add(backup)
    Session.commit()

