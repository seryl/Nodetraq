import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PoolsController(BaseController):

    def index(self):
        c.title = "Nodetraq -- Pools"
        c.selected_page = "pools"
        c.subpage = "top"
        return render('/pools/top.mako')
