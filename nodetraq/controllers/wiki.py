import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level

log = logging.getLogger(__name__)

class WikiController(BaseController):

    @user_level(0)
    def __before__(self):
        super(WikiController, self).__before__()

    def index(self):
        c.title = 'nodetraq - Wiki'
        c.selected_page = 'wiki'
        c.subpage = 'index'
        return render('/wiki/index.mako')

