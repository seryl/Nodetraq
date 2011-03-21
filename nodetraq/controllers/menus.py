import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import rest

from nodetraq.lib.base import BaseController, render
from nodetraq.lib.F5 import LoadBalancer
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node, Group, Studio, Game

log = logging.getLogger(__name__)

class MenusController(BaseController):

    @rest.restrict('POST')
    def grouplist(self):
        c.groups = Session.query(Group.name).order_by('name').all()
        return render('/menus/group/grouplist.mako')

    @rest.restrict('POST')
    def loadbalancerlist(self):
        lb = LoadBalancer(ip='your_f5_lb')
        c.loadbalancers = lb.get_pools()
        c.loadbalancers.sort()
        return render('/menus/loadbalancer/list.mako')

    @rest.restrict('POST')
    def batcheditlist(self):
        return render('/menus/batchedit/list.mako')

    @rest.restrict('POST')
    def nagios(self):
        return render('/menus/nagios/list.mako')

    @rest.restrict('POST')
    def studios(self):
        c.studios = [ ('', '') ]
        for studio in Session.query(Studio).all():
            c.studios.append((studio.id, studio.name))

        return render('/menus/studios/list.mako')

    @rest.restrict('POST')
    def games(self):
        c.games = [ ('', '') ]
        for game in Session.query(Game).all():
            c.games.append((game.id, game.name))

        return render('/menus/games/list.mako')

