import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render

log = logging.getLogger(__name__)

class InventoryController(BaseController):

    def index(self):
        c.title = 'Nodetraq - Inventory'
        c.selected_page = 'inventory'
        c.subpage = 'index'
        return render('/inventory/list.mako')
