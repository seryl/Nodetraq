import logging
from time import time

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node, Group
from nodetraq.model.graphs import Graph

from nodetraq.lib.drraw import generate_rrd_sequence_map, rrd_types, generate_index, grab_new_drraw

log = logging.getLogger(__name__)

class GraphsController(BaseController):

    @user_level(0)
    def index(self):
        c.title = 'Nodetraq -- Graphs'
        c.selected_page = 'graphs'
        c.subpage = 'index'

        c.graphs = Session.query(Graph).all()
        return render('/graphs/index.mako')

    @user_level(0)
    def new(self):
        c.title = 'Nodetraq -- Graphs'
        c.selected_page = 'graphs'
        c.subpage = 'new'

        c.groups = Session.query(Group)\
            .order_by('name').all()

        c.rrd_types = rrd_types

        return render('/graphs/new.mako')

    @user_level(0)
    def create(self):
        graph_title = ''
        rrds = []
        group = None
        for k,v in request.params.iteritems():
            if k == 'rrd_type':
                rrds.append(v)
            elif k == 'graph_title':
                graph_title = v
            elif k == 'group_select':
                group = Session.query(Group)\
                    .filter(Group.name == v).first()
            else:
                pass

        graph = Graph()
        graph.name = graph_title
        graph.filename = 'g%s' % time()
        graph.rrd_types = ','.join(rrds)
        graph.group = group

        if not graph.name or not graph.rrd_types or not graph.group:
            session['flash'] = "Failed to created graph"
            session.save()
            return redirect(url(
                    controller='graphs', action='index'))

        Session.add(graph)
        Session.commit()
        session['flash'] = "Successfully created %s" % graph.name
        session.save()
        grab_new_drraw(graph)
        generate_index()
        return redirect(url(
                controller='graphs', action='index'))

    @user_level(0)
    def edit(self, id):
        c.title = 'Nodetraq -- Graphs'
        c.selected_page = 'graphs'
        c.subpage = 'edit'

        if id.isdigit():
            c.graph = Session.query(Graph)\
                .filter(Graph.id == int(id)).first()
        else:
            c.graph = Session.query(Graph)\
                .filter(Graph.name == id).first()

        c.groups = Session.query(Group)\
            .order_by('name').all()

        c.rrd_types = rrd_types
        return render('/graphs/edit.mako')

    @user_level(0)
    def update(self):
        id = request.params['id']
        graph = Session.query(Graph)\
            .filter(Graph.id == id).first()
        group = request.params['group_select']

        graph.name = request.params['graph_title']
        graph.filename = request.params['filename']
        graph.group = Session.query(Group)\
            .filter(Group.name == group).first()

        rrds = []
        for k,v in request.params.iteritems():
            if k == 'rrd_type':
                rrds.append(v)

        graph.rrd_types = ','.join(rrds)

        if not graph.name or not graph.group or not graph.rrd_types:
            session['flash'] = "Failed to update graph"
            session.save()
            return redirect(url(
                    controller='graphs', action='index'))

        Session.add(graph)
        Session.commit()
        session['flash'] = "Successfully updated"
        session.save()
        grab_new_drraw(graph)
        generate_index()
        return redirect(url(
                controller='graphs', action='index'))

    @user_level(0)
    def delete(self, id):
        if id.isdigit():
            graph = Session.query(Graph)\
                .filter(Graph.id == int(id)).first()
        else:
            graph = Session.query(Graph)\
                .filter(Graph.name == id).first()

        Session.delete(graph)
        Session.commit()
        session['flash'] = "Successfully deleted %s" % graph.name
        session.save()
        return redirect(url(
                controller='graphs', action='index'))

    @user_level(0)
    def show(self, id=None):
        c.title = 'Nodetraq -- Graphs'
        c.selected_page = 'graphs'
        c.subpage = 'show'

        c.graph = None
        if id:
            if id.isdigit():
                c.graph = Session.query(Graph)\
                    .filter(Graph.id == int(id)).first()
            else:
                c.graph = Session.query(Graph)\
                    .filter(Graph.name == id).first()

        c.graph_list = Session.query(Graph).all()
        return render('/graphs/show.mako')

    def rrd_file(self, id):
        response.content_type = 'text/plain'

        if id.isdigit():
            graph_data = Session.query(Graph)\
                .filter(Graph.id == int(id)).first()
        else:
            graph_data = Session.query(Graph)\
                .filter(Graph.name == id).first()

        c.graph = graph_data.filename[1:]
        hostnames = [n.hostname for n in graph_data.get_hosts()]

        c.datasource = generate_rrd_sequence_map(
            hostnames, graph_data.get_rrds())

        c.title = graph_data.name

        if len(c.datasource) == 2:
            c.colors = ['Lime', 'Red']
            c.brmod = 2
        else:
            c.colors = ['Lime', 'Teal', 'Maroon']
            c.brmod = 3

        return render('/graphs/graph.mako')
