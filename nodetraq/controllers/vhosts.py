import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level

from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node, NodeVhost

log = logging.getLogger(__name__)

class VhostsController(BaseController):

    @user_level(0)
    def __before__(self):
        super(self.__class__, self).__before__()

    def index(self, id):
        c.title = 'Nodetraq - vhosts'
        c.selected_page = 'nodes'
        c.subpage = 'vhosts'
        c.header = 'Nodes : vhosts'
        c.node = Session.query(Node).filter(Node.id == id).first()
        c.node_id = c.node.id

        return render('/nodes/vhosts/index.mako')

    def new(self, id):
        c.title = 'Nodetraq - vhosts'
        c.selected_page = 'nodes'
        c.subpage = 'vhosts'
        c.header = 'Nodes:vhosts'
        c.node_id = id

        return render('/nodes/vhosts/new.mako')

    def create(self, id):
        node = Session.query(Node).filter(Node.id == id).first()
        if not node.vhosts:
            node.vhosts = []

        vhost = NodeVhost()
        vhost.node = node
        vhost.hostname = request.params['hostname']
        vhost.comment = request.params['comment']

        node.vhosts.append(vhost)
        Session.add(node)
        Session.commit()

        return redirect(url(controller='vhosts', action='index', id=id))

    def edit(self, id, vhostid=None):
        c.title = 'Nodetraq - Vhost - Edit'
        c.selected_page = 'nodes'
        c.subpage = 'vhost'
        c.header = 'Edit Vhost'
        c.vhostid = vhostid
        c.node_id = id
        c.vhost = Session.query(NodeVhost)\
                .filter(NodeVhost.id == vhostid).first()

        return render('/nodes/vhosts/edit.mako')

    def show(self, id, vhostid=None):
        c.title = 'Nodetraq - Vhost - Edit'
        c.selected_page = 'nodes'
        c.subpage = 'vhost'
        c.header = 'Show Vhost'
        c.vhostid = vhostid
        c.node_id = id
        return render('/nodes/vhosts/show.mako')

    def update(self, id, vhostid=None):
        return None

