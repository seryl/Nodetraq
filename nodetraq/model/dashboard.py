from sqlalchemy import Column, Table, String, Integer,\
    Float, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from nodetraq.model.meta import Base, now

flag_lookup = Table (
    'flag_lookups', Base.metadata,
    Column('node_flag_info_id', Integer, ForeignKey('node_flag_info.id')),
    Column('flag_id', Integer, ForeignKey('flags.id')),
    )

node_flags_lookup = Table (
    'flagged_node_lookups', Base.metadata,
    Column('node_id', Integer, ForeignKey('nodes.id')),
    Column('node_flag_info_id', Integer, ForeignKey('node_flag_info.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
    )

class NodeFlagInfo(Base):
    __tablename__ = 'node_flag_info'

    id = Column(Integer, primary_key=True)
    user = relationship('User', secondary=node_flags_lookup, uselist=False)
    description = Column(String(255))
    flags = relationship('Flag', secondary=flag_lookup)

class Flag(Base):
    __tablename__ = 'flags'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))


