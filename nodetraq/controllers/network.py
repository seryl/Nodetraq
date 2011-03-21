import logging
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from nodetraq.lib.base import BaseController, render

from nodetraq.model.meta import Session
from nodetraq.model.network import NetworkDevice

log = logging.getLogger(__name__)

class NetworkController(BaseController):

    def index(self):
        c.title = 'Nodetraq - Network'
        c.selected_page = 'network'
        c.subpage = 'index'

        c.network_devices = Session.query(NetworkDevice).all()
        return render('/network/index.mako')

    def new(self):
        c.title = 'Nodetraq - New Network Device'
        c.selected_page = 'network'
        c.subpage = 'new'

        c.parents = [('','')]
        for parent in [
            (d.id, d.hostname) for d in \
                Session.query(NetworkDevice).filter(
                    NetworkDevice.logical == False).all()]:
            c.parents.append(parent)
        return render('/network/new.mako')

    def edit(self, id):
        c.title = 'Nodetraq - New Network Device'
        c.selected_page = 'network'
        c.subpage = 'edit'

        c.network_device = Session.query(NetworkDevice).filter(
            NetworkDevice.id == id).first()
        c.parents = [('','')]
        for parent in [
            (d.id, d.hostname) for d in \
                Session.query(NetworkDevice).filter(
                    NetworkDevice.logical == False).all()]:
            c.parents.append(parent)
        return render('/network/edit.mako')

    def show(self, id):
        c.title = 'Nodetraq - Network Devices'
        c.selected_page = 'network'
        c.subpage = 'show'

        c.network_device = Session.query(NetworkDevice).filter(
            id == NetworkDevice.id).first()
        return render('/network/show.mako')

    @jsonify
    def create(self):
        p = ['_hostname', 'logical',
         'management_ip', 'type',
         'serial_number', 'part_number',
         'mac_address', 'parent']

        try:
            data = json.loads(request.params.items()[0][0])['data']
        except:
            return {'success': False}

        network_device = NetworkDevice()
        count = 0
        for param in p:
            if param in data:
                if param == 'parent':
                    if not data[param]:
                        network_device.parent = None
                        continue
                    else:
                        network_device.parent = Session.query(
                            NetworkDevice).filter(
                            NetworkDevice.id == int(
                                    data[param])).first()
                        continue
                setattr(network_device,
                        param, data[param])
                count += 1
        if count:
            Session.add(network_device)
            Session.commit()
            return {'success': True}
        return {'success': False}

    @jsonify
    def update(self, id):
        p = ['_hostname', 'logical',
         'management_ip', 'type',
         'serial_number', 'part_number',
         'mac_address', 'parent']
        try:
            data = json.loads(
                request.params.items()[0][0])['data']
        except:
            return {'success': False}

        network_device = Session.query(NetworkDevice).filter(
            NetworkDevice.id == id).first()
        if not network_device:
            return {'success': False}

        count = 0
        for param in p:
            if param in data:
                if param == 'parent':
                    if not data[param]:
                        network_device.parent = None
                        continue
                    else:
                        network_device.parent = Session.query(
                            NetworkDevice).filter(
                            NetworkDevice.id == int(
                                    data[param])).first()
                        continue
                setattr(network_device,
                        param, data[param])
                count += 1
        if count:
            Session.add(network_device)
            Session.commit()
            return {'success': True}
        return {'success': False}

    @jsonify
    def destroy(self, id):
        network_device = Session.query(NetworkDevice).filter(
            NetworkDevice.id == id).first()
        Session.delete(network_device)
        Session.commit()
        return {'success': True}
