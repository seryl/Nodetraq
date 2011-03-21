import json
import re

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from sqlalchemy import Column, Table, String, Integer,\
        Float, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from nodetraq.model.meta import Base, Session, now
from nodetraq.model.activity import Activity
from nodetraq.model.users import User
from nodetraq.model.dashboard import NodeFlagInfo, node_flags_lookup
from nodetraq.lib.util.network import str_to_mac

# Tables
node_groups = Table (
    'node_groups', Base.metadata,
    Column('node_id', Integer, ForeignKey('nodes.id')),
    Column('group_id', Integer, ForeignKey('groups.id')),
    )

node_comments_lookup = Table (
    'node_comments_lookup', Base.metadata,
    Column('node_id', Integer, ForeignKey('nodes.id')),
    Column('node_comments_id', Integer, ForeignKey('node_comments.id')),
    )

node_vhosts_lookup = Table (
    'node_vhosts_lookup', Base.metadata,
    Column('node_id', Integer, ForeignKey('nodes.id')),
    Column('node_vhosts_id', Integer, ForeignKey('node_vhosts.id')),
    )

node_dbbackup_lookup = Table (
    'node_dbbackup_lookup', Base.metadata,
    Column('node_id', Integer, ForeignKey('nodes.id')),
    Column('node_dbbackups_id', Integer, ForeignKey('node_dbbackups.id')),
    )

node_dbbackup_locations = Table (
    'node_dbbackup_location', Base.metadata,
    Column('server_id', Integer, ForeignKey('nodes.id')),
    Column('node_dbbackups_id', Integer, ForeignKey('node_dbbackups.id')),
    )

node_lbpools_lookup = Table (
    'node_lbpools_lookup', Base.metadata,
    Column('node_id', Integer, ForeignKey('nodes.id')),
    Column('node_lbpools_id', Integer, ForeignKey('lb_pools.id')),
    )

node_lbpools_comments_lookup = Table (
    'node_lbpools_comments_lookup', Base.metadata,
    Column('lb_pool_id', Integer, ForeignKey('lb_pools.id')),
    Column('lb_pool_comments_id', Integer, ForeignKey('lb_pool_comments.id')),
    )

node_disk_lookup = Table (
    'node_disk_lookup', Base.metadata,
    Column('node_id', Integer, ForeignKey('nodes.id')),
    Column('disk_id', Integer, ForeignKey('disks.id')),
    )

disk_controller_lookup = Table (
    'disk_controller_lookup', Base.metadata,
    Column('disk_id', Integer, ForeignKey('disks.id')),
    Column('disk_controller_id', Integer, ForeignKey('disk_controllers.id')),
    )

studio_game_lookup = Table (
    'studio_game_lookup', Base.metadata,
    Column('studio_id', Integer, ForeignKey('studios.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
    )

game_node_lookup = Table (
    'game_node_lookup', Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('node_id', Integer, ForeignKey('nodes.id'))
    )

class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=now())
    updated_at = Column(TIMESTAMP, onupdate=now())

    # Host info
    hostname = Column(String(50))
    reported_hostname = Column(String(50))
    model_name = Column(String(50))
    service_tag = Column(String(50))
    location = Column(String(20))
    rack = Column(Integer)
    rack_u = Column(Integer)
    xen_instance = Column(Integer)
    description = Column(String(255))
    firmware = Column(String(255))
    root_password = Column(String(255))

    # Network
    primary_ip = Column(String(20))
    reported_primary_ip = Column(String(20))
    secondary_ip = Column(String(20))
    reported_secondary_ip = Column(String(20))
    primary_mac = Column(String(20))
    reported_primary_mac = Column(String(20))
    secondary_mac = Column(String(20))
    reported_secondary_mac = Column(String(20))
    drac_ip = Column(String(20))
    reported_drac_ip = Column(String(20))
    drac_switch = Column(String(20))
    drac_port = Column(String(20))
    vhosts = relationship('NodeVhost',
            secondary=node_vhosts_lookup,
            backref=backref('node', uselist=False))
    lb_pools = relationship('LBPool',
            secondary=node_lbpools_lookup,
            backref=backref('nodes'))

    # Cpu
    cpu_processor = Column(String(50))
    cpu_count = Column(Integer)
    memory = Column(Float)

    # Disk Information
    disks = relationship('Disk',
            secondary=node_disk_lookup,
            backref=backref('node', uselist=False))

    # Operating System
    ssh_key = Column(Text)
    puppet_key = Column(Text)
    server_license = Column(String(255))
    sql_license = Column(String(255))

    # Database Info
    db_backups = relationship('NodeDatabaseBackup',
        secondary=node_dbbackup_lookup,
        backref=backref('server', uselist=False),
        lazy=True,
        cascade='all, delete')

    # Services
    nagios = Column(Boolean, default=False)
    puppet = Column(Boolean, default=True)

    # Information
    groups = relationship('Group', secondary=node_groups,
        backref=backref('nodes', lazy=True),
        lazy=True)
    flags = relationship('NodeFlagInfo', secondary=node_flags_lookup,
        backref=backref('node', lazy=True, uselist=False),
        cascade="all, delete-orphan", single_parent=True)
    comments = relationship('NodeComment',
        secondary=node_comments_lookup,
        backref=backref('node', lazy=True, uselist=False),
        cascade="all, delete-orphan", single_parent=True)

    @property
    def server_id(self):
        if self.rack == None:
            self.rack = 0
        if self.rack_u == None:
            self.rack_u = 0
        if self.xen_instance == None\
            or self.xen_instance == ''\
            or self.xen_instance == 0:
            return '%s%03d%02d' % (self.location,self.rack,self.rack_u)
        else:
            return '%s%03d%02d.%02d' % (self.location, self.rack,
                self.rack_u, self.xen_instance)

    @property
    def sync_issues(self):
        issues = []
        for item in [
            (self.reported_hostname, self.hostname, 'hostname'),
            (self.reported_primary_ip, self.primary_ip, 'primary ip'),
            (self.reported_secondary_ip, self.secondary_ip, 'secondary ip'),
            (self.reported_primary_mac, self.primary_mac, 'primary mac'),
            (self.reported_secondary_mac, self.secondary_mac, 'secondary mac')]:
            reported = item[0] or None
            value = item[1] or None
            if item[2] in ['primary mac', 'secondary mac']:
                value = str_to_mac(value)
            if reported != value:
                issues.append({
                        'reported': reported,
                        'value': value,
                        'type': item[2]
                        })
        return issues

    def _sanitize(self):
        self.primary_mac = self.primary_mac.replace(':', '')
        self.secondary_mac = self.secondary_mac.replace(':', '')

    def update_disks(self, diskinfo):
        if self.disks:
            current_serials = [ d.serial_no for d in self.disks ]
            new_serials = [ d['serial_no'] for d in diskinfo['disks'] ]
            diff_serials = list(set(new_serials) - set(current_serials))
            remove_serials = [ serial for serial in current_serials \
                                   if serial not in new_serials ]

            for s in remove_serials:
                for rd in self.disks:
                    if rd.serial_no == s:
                        self.disks.remove(rd)
                        Session.delete(rd)

            for s in diff_serials:
                for disk in diskinfo['disks']:
                    if disk['serial_no'] == s:
                        new_disk = Disk()
                        new_disk.serial_no = disk['serial_no']
                        new_disk.capacity = disk['capacity']
                        new_disk.type = disk['type']
                        new_disk.controller_slot = disk['controller_slot']
                        new_disk.controller_id = DiskController\
                            .grab_controller(disk['controller'])
                        Session.add(new_disk)
                        self.disks.append(new_disk)

        else:
            self.disks = []
            for disk in diskinfo['disks']:
                new_disk = Disk()
                new_disk.serial_no = disk['serial_no']
                new_disk.capacity = disk['capacity']
                new_disk.type = disk['type']
                new_disk.controller_slot = disk['controller_slot']
                new_disk.controller_id = DiskController\
                    .grab_controller(disk['controller'])
                Session.add(new_disk)
                self.disks.append(new_disk)

        Session.add(self)
        Session.commit()

    def __json__(self, format=False):
        ignore_list = ('metadata', 'update_disks')
        keys = [v for v in dir(self) if not v.startswith('_')]
        keys = [v for v in keys if not v in ignore_list]

        json_hash = {}
        for key in keys:
            if key == 'groups':
                groups = []
                for group in self.__getattribute__(key):
                    groups.append(group.name)
                    json_hash[key] = groups
            else:
                json_hash[key] = '%s' % self.__getattribute__(key)

        if format:
            return json.dumps(json_hash, sort_keys=True, indent=4)
        return json_hash

    def __xml__(self):
        ignore_list = ('server_id', 'metadata')
        root = ET.Element("node")

        keys = [v for v in dir(self) if not v.startswith('_')]
        keys = [v for v in keys if not v in ignore_list]

        for key in keys:
            elem = ET.SubElement(root, key)
            elem.text = '%s' % getattr(self, key)

        tree = ET.ElementTree(root)
        txt = ET.tostring(root)
        return parseString(txt).toprettyxml()

    def __repr__(self):
        return """<Node( { 'hostname': '%s',
        'nagios': %s,
        'primary_ip': %s,
        'secondary_ip': %s,
        'primary_mac': %s,
        'secondary_mac': %s,
        'description': %s,
        'drac_ip': %s,
        'rack': %s
        'rack_u': %s,
    })>
    """ % ( self.hostname, self.nagios,\
            self.primary_ip, self.secondary_ip, self.primary_mac, \
            self.secondary_mac, self.description, \
            self.drac_ip, self.rack, self.rack_u)

class Group(Base):
    __tablename__ = 'groups'
    __table_args__ = {'useexisting': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))

    def __repr__(self):
        return "%s" % self.name

class NodeComment(Base):
    __tablename__ = 'node_comments'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=now())
    updated_at = Column(TIMESTAMP, onupdate=now())
    node_id = Column(Integer, ForeignKey('nodes.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        User, primaryjoin=user_id == User.id)
    description = Column(Text)

    def __repr__(self):
        return self.description

class NodeVhost(Base):
    __tablename__ = 'node_vhosts'

    id = Column(Integer, primary_key=True)
    node_id = Column(Integer, ForeignKey('nodes.id'))
    hostname = Column(String(255))
    comment = Column(String(255))

class BackupType(Base):
    __tablename__ = 'backup_types'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class NodeDatabaseBackup(Base):
    __tablename__ = 'node_dbbackups'

    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, default=True)
    server_id = Column(Integer, ForeignKey('nodes.id'))
    storage_id = Column(Integer, ForeignKey('nodes.id'))
    storage = relationship('Node', primaryjoin=storage_id == Node.id)
    directory = Column(String(255))
    backup_type_id = Column(Integer, ForeignKey('backup_types.id'))
    backup_type = relationship(
        'BackupType', primaryjoin=backup_type_id == BackupType.id)

class NodeDatabaseBackupHistory(Base):
    __tablename__ = 'node_dbbackup_history'

    id = Column(Integer, primary_key=True)
    dbbackup_id = Column(Integer, ForeignKey('node_dbbackups.id'))
    backup_start = Column(TIMESTAMP, default=now())
    backup_end = Column(TIMESTAMP, onupdate=now())
    size = Column(String(16), default='0')

class NodeImport(Base):
    __tablename__ = 'node_imports'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    description = Column(String(255))

    def __repr__(self):
        return 'file: %s, description: %s' % (
                self.filename, self.description)

class LBPool(Base):
    __tablename__ = 'lb_pools'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))

class LBPoolComments(Base):
    __tablename__ = 'lb_pool_comments'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=now())
    updated_at = Column(TIMESTAMP, onupdate=now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        User, primaryjoin=user_id == User.id)
    comment = Column(String(255))

class DiskController(Base):
    __tablename__ = 'disk_controllers'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    @classmethod
    def grab_controller(cls, controller_name):
        if not controller_name:
            return None

        controller = Session.query(cls)\
            .filter(cls.name == controller_name)\
            .first()

        if controller:
            return controller.id
        else:
            c = cls()
            c.name = controller_name
            Session.add(c)
            Session.commit()
            return c.id

class Disk(Base):
    __tablename__ = 'disks'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=now())
    serial_no = Column(String(50))
    capacity = Column(String(50))
    type = Column(String(20))
    controller_id = Column(Integer, ForeignKey('disk_controllers.id'))
    controller_slot = Column(Integer)
    controller = relationship(
        'DiskController', primaryjoin=controller_id == DiskController.id)

    @property
    def get_capacity():
        if not self.capacity:
            return None
        regex = '(\d+.\d+|\d+) GB'
        cap_result = re.search(regex, self.capacity)
        if not cap_result:
            return None
        else:
            return float(cap_result.groups(0)[0])

    def __repr__(self):
        return '<Disk {"capacity": "%s", "serial_no": "%s", "type": "%s"} >' \
            % (self.capacity, self.serial_no, self.type)

class Studio(Base):
    __tablename__ = 'studios'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    games = relationship('Game',
            secondary=studio_game_lookup,
            backref=backref('studio', uselist=False))

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    nodes = relationship('Node',
            secondary=game_node_lookup,
            backref=backref('game', uselist=False))

