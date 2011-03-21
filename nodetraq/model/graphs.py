from sqlalchemy import Column, Table, String, Integer,\
    Float, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from nodetraq.model.meta import Base, Session
from nodetraq.model.nodes import Group

class Graph(Base):
    __tablename__ = 'graphs'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP)
    name = Column(String(255))
    filename = Column(String(255))
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(
            Group, primaryjoin=group_id == Group.id)
    rrd_types = Column(Text)

    def get_hosts(self):
        return self.group.nodes

    def get_rrds(self):
        return self.rrd_types.split(',')

