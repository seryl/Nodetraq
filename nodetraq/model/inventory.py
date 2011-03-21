from sqlalchemy import Column, Table, String, Integer,\
    Float, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from nodetraq.model.meta import Base

inventory_lookup = Table (
    'inventory_lookup', Base.metadata,
    Column('inventory_id', Integer, ForeignKey('inventory.id')),
    Column('inventory_type', Integer, ForeignKey('inventory_type.id')),
    Column('inventory_type_item', Integer, ForeignKey('inventory_type_item.id')),
    )

class InventoryItem(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP)
    description = Column(String(255))

class InventoryType(Base):
    __tablename__ = 'intenvory_types'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))

class HardDrive(Base):
    __tablename__ = 'inventory_harddrives'

    id = Column(Integer, primary_key=True)

class InventoryUpdate(Base):
    __tablename__ = 'inventory_updates'

    id = Column(Integer, primary_key=True)
    inventory_id = Column(ForeignKey('inventory.id'))
    inventory = relationship(
            Inventory, primaryjoin=inventory_id == Inventory.id)

class Inventory(object):
    pass


