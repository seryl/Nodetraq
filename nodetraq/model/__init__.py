"""The application's model objects"""
from nodetraq.model.meta import Session, metadata, Base
from nodetraq.model.nodes import Group, Node, Disk, DiskController
from nodetraq.model.users import User
from nodetraq.model.activity import ActivityType, Changeset, Activity
from nodetraq.model.graphs import Graph
from nodetraq.model.network import NetworkDevice, NetworkDeviceIpInfo, NetworkDeviceMacInfo

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)


