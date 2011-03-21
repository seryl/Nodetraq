import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level

log = logging.getLogger(__name__)

class HelpController(BaseController):

    @user_level(0)
    def __before__(self):
        super(self.__class__, self).__before__()

    def index(self):
        c.title = 'Nodetraq - Help'
        c.selected_page = 'help'
        c.subpage = 'index'
        return render('/help/index.mako')

    def search(self):
        c.title = 'Nodetraq - Help - Search'
        c.selected_page = 'help'
        c.subpage = 'search'
        return render('/help/search.mako')
