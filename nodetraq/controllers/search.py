import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render
from nodetraq.model.meta import Session, metadata
from nodetraq.model.nodes import Node, Group

log = logging.getLogger(__name__)

class SearchController(BaseController):

    def index(self):
        c.title = 'Nodetraq - Search'
        c.selected_page = 'search'
        c.subpage = 'index'
        return render('/search/index.mako')

    def activity(self):
        return 'activity'

    def groups(self):
        return 'groups'

    def nodes(self):
        return 'nodes'
