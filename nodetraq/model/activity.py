from sqlalchemy import Column, Table, String, Integer,\
    Float, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import and_
from datetime import timedelta

from nodetraq.model.meta import Base, Session, now
from nodetraq.model.users import User

activity_changesets = Table (
    'activity_changesets', Base.metadata,
    Column('activity_id', Integer, ForeignKey('activity.id')),
    Column('changeset_id', Integer, ForeignKey('changesets.id')),
    )

class ActivityType(Base):
    __tablename__ = 'activity_types'
    __tableargs__ = (
            UniqueConstraint('name', 'action'),
            )

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    action = Column(String(50))

class Changeset(Base):
    __tablename__ = 'changesets'

    id = Column(Integer, primary_key=True)
    field = Column(String(255))
    old_value = Column(String(255))
    new_value = Column(String(255))

class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=now)
    parent_id = Column(Integer, ForeignKey('activity.id'))
    parent = relationship('Activity', remote_side=[id], backref="children")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', primaryjoin=user_id == User.id)
    activity_type_id = Column(Integer, ForeignKey('activity_types.id'))
    activity_type = relationship(ActivityType,
            primaryjoin=activity_type_id == ActivityType.id)
    changesets = relationship('Changeset',
            secondary=activity_changesets,
            backref='activity')
    link = Column(String(255))

    @classmethod
    def get_activity_page(cls, date_from=None, date_to=None):
        if not (date_from or date_to):
            activity = Session.query(cls)\
                .filter(and_(
                    cls.created_at < now(),
                    cls.created_at > now() - timedelta(days=3),
                    cls.parent_id == None)).all()
        elif date_from:
            if not date_to:
                activity = Session.query(cls)\
                    .filter(and_(
                        cls.created_at < date_from,
                        cls.created_at > date_from - timedelta(days=3),
                        cls.parent_id == None)).all()
            else:
                activity = Session.query(cls)\
                    .filter(and_(
                        cls.created_at < date_from,
                        cls.created_at > date_to,
                        cls.parent_id == None)).all()
        else:
            return None

        return activity
