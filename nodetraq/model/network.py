import json

from sqlalchemy import Column, Table, String, Integer,\
        Float, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from nodetraq.model.meta import Base, Session, now
from nodetraq.lib.activity import Activity
from nodetraq.model.users import User
from nodetraq.lib.util.network import str_to_mac


class NetworkDeviceMacInfo(Base):
    __tablename__ = 'network_device_mac_list'

    id = Column(Integer, primary_key = True)
    network_device_id = Column(Integer, ForeignKey('network_devices.id'))
    mac_address = Column(String(50))

class NetworkDeviceIpInfo(Base):
    __tablename__ = 'network_device_ip_list'

    id = Column(Integer, primary_key = True)
    network_device_id = Column(Integer, ForeignKey('network_devices.id'))
    mac_address = Column(String(50))

class NetworkSubdevice(Base):
    __tablename__ = 'network_subdevices'

    id = Column(Integer, primary_key = True)
    parent_id = Column(Integer, ForeignKey('network_devices.id'))
    child_id = Column(Integer, ForeignKey('network_devices.id'))

class NetworkDevice(Base):
    __tablename__ = 'network_devices'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=now())
    updated_at = Column(TIMESTAMP, onupdate=now())
    _hostname = Column(String(50))
    logical = Column(Boolean, default=False)

    management_ip = Column(String(50))
    mac_address = Column(String(50))
    type = Column(String(50))
    serial_number = Column(String(50))
    part_number = Column(String(50))

    parent_id = Column(Integer, ForeignKey('network_devices.id'))
    parent = relationship(
        'NetworkDevice', remote_side=[id], backref="children")

    def _Get_hostname(self):
        if self._hostname:
            return self._hostname
        return self.management_ip

    def _Set_hostname(self, value):
        if not value:
            return False
        self._hostname = str(value)
        return True

    hostname = property(_Get_hostname, _Set_hostname)

    mac_address_list = relationship(
        NetworkDeviceMacInfo,
        primaryjoin=\
            id==NetworkDeviceMacInfo.network_device_id)

    ip_address_list = relationship(
        NetworkDeviceIpInfo,
        primaryjoin=\
            id==NetworkDeviceIpInfo.network_device_id)
