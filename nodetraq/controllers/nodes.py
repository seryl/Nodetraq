import logging
import os
import shutil
import json
from urllib import urlencode

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config
from pylons.decorators import jsonify

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.model.meta import Session, metadata
from nodetraq.model.nodes import Node, Group, NodeComment, NodeDatabaseBackup, Studio, Game
from nodetraq.model.users import User
from nodetraq.model.dashboard import NodeFlagInfo, Flag
from nodetraq.lib.activity import ActivityEngine
from nodetraq.lib.util.csv_import import node_insert_db, node_csv_import
from nodetraq.lib.util.csv_export import export_node
from nodetraq.lib.query import get_fields_and_query

from sqlalchemy.sql.expression import asc, desc

log = logging.getLogger(__name__)

csv_store = ''.join([config['pylons.paths']['uploads'], '/nodes/'])

class NodesController(BaseController):

    def __before__(self):
        super(self.__class__, self).__before__()

    @user_level(0)
    def index(self, format='html'):
        c.title = 'Nodetraq - Nodes'
        c.selected_page = 'nodes'
        c.subpage = 'list'
        c.header = 'Nodes'
        c.filters = [
            { 'name': 'hostname', 'label': 'Hostname', 'type': 'text' },
            { 'name': 'groups', 'label': 'Group', 'type': 'text' },
            { 'name': 'primary_ip', 'label': 'Primary IP', 'type': 'text' },
            { 'name': 'primary_mac', 'label': 'Primary MAC', 'type': 'text' },
            { 'name': 'secondary_ip', 'label': 'Secondary IP', 'type': 'text' },
            { 'name': 'secondary_mac', 'label': 'Secondary MAC', 'type': 'text' },
            { 'name': 'location', 'label': 'Location', 'type': 'text' },
            { 'name': 'rack', 'label': 'Rack', 'type': 'integer' },
            { 'name': 'rack_u', 'label': 'Rack U', 'type': 'integer' },
            { 'name': 'service_tag', 'label': 'Service Tag', 'type': 'text' },
            { 'name': 'cpu_count', 'label': 'Cpu Count', 'type': 'integer' },
            { 'name': 'cpu_speed', 'label': 'Cpu Speed', 'type': 'integer' },
            { 'name': 'memory', 'label': 'Memory', 'type': 'integer' }, ]

        is_sorted = False
        query, c.search_fields = get_fields_and_query(Session,
                Node, request.params)
        c.request_url = request.environ.get('PATH_INFO')
        if request.environ.get('QUERY_STRING'):
            c.request_url +=  '?' + request.environ['QUERY_STRING']
        c.node_count = query.count()

        c.link_append = '&' + urlencode(
            [p for p in request.params.items()\
                 if p[0] != 'page'])

        if c.link_append == '&':
            c.link_append = None

        if 'sort' in request.params:
            sortkey, sortorder = request.params['sort'].split(':')
            is_sorted = True
            c.sort_order = sortorder
        else:
            c.sort_order = None

        if 'show_all' in request.params:
            c.page = 1
            c.total_pages = 1
            c.current_page_count = 1
            if is_sorted:
                if sortorder == 'asc':
                    c.nodes = query.order_by(asc(sortkey)).all()
                else:
                    c.nodes = query.order_by(desc(sortkey)).all()
            else:
                c.nodes = query.order_by('hostname').all()
        else:
            c.page = int(request.params['page'])\
                    if 'page' in request.params else 1
            c.total_pages = (c.node_count+25-1)/25
            c.current_page_count = (c.page-1)*25
            if is_sorted:
                if sortorder == 'asc':
                    c.nodes = query.order_by(asc(sortkey))\
                        [c.current_page_count:c.current_page_count+25]
                else:
                    c.nodes = query.order_by(desc(sortkey))\
                        [c.current_page_count:c.current_page_count+25]
            else:
                c.nodes = query.order_by('hostname')\
                    [c.current_page_count:c.current_page_count+25]

        c.group_list = [g[0] for g in Session.query(Group.name)\
                .order_by('name')]

        if format == 'html':
            return render('/nodes/list.mako')
        elif format == 'json':
            response.content_type = 'application/json'
            return render('/nodes/list.json')
        elif format == 'xml':
            response.content_type = 'application/xml'
            return render('/nodes/list.xml')

    @user_level(0)
    def edit(self, id):
        c.node = Session.query(Node).filter(Node.id == id).first()
        c.title = 'Nodetraq - Edit node'
        c.selected_page = 'nodes'
        c.subpage = 'edit'
        c.game_list = [ ('', '') ]
        for game in Session.query(Game).all():
            c.game_list.append((game.id, game.name))

        c.selected_game = 0
        if c.node.game:
            for game in c.game_list:
                if game[1] == c.node.game.name:
                    c.selected_game = game[0]
                    break

        return render('/nodes/edit.mako')

    @user_level(0)
    def show(self, id, format='html'):
        if id.isdigit():
            c.node = Session.query(Node).filter(Node.id == id).first()
        else:
            c.node = Session.query(Node).filter(Node.hostname == id).first()
        c.title = 'Nodetraq - Show nodes'
        c.selected_page = 'nodes'
        c.subpage = 'show'

        if format == 'html':
            c.current_user = session['active_user']
            return render('/nodes/show.mako')
        elif format == 'json':
            response.content_type = 'application/json'
            return c.node.__json__(format=True)
        elif format == 'xml':
            response.content_type = 'application/xml'
            return c.node.__xml__()

    @user_level(0)
    def namelist(self, format='mako'):
        c.nodes = Session.query(Node.hostname).all()
        if format == 'json':
            response.content_type = 'application/json'
        elif format == 'xml':
            response.content_type = 'application/xml'
        return render('/nodes/namelist/list.' + format)

    @user_level(0)
    def new(self):
        c.title = 'Nodetraq - New node'
        c.selected_page = 'nodes'
        c.subpage = 'new'
        return render('/nodes/new.mako')

    @user_level(0)
    def importcsv(self):
        c.title = 'Nodetraq - Import nodes'
        c.selected_page = 'nodes'
        c.subpage = 'importcsv'
        return render('/nodes/import.mako')

    @user_level(0)
    def upload_csv(self):
        # TODO: Make sure you check for existing files
        myfile = request.params['uploaded_file']
        filename = myfile.filename.lstrip(os.sep)
        save_location = os.path.join(csv_store, filename)
        permanent_file = open(save_location, 'w')

        shutil.copyfileobj(myfile.file, permanent_file)
        myfile.file.close()
        permanent_file.close()

        node_insert_db(node_csv_import(save_location))

        # TODO: Write description to database as well as file location.
        # request.params['description']
        return redirect(url(controller='nodes', action='index'))

    @user_level(0)
    def export_csv(self):
        # TODO: This isn't complete.
        if request.params.has_key('ids[]'):
            id_list = [v for k,v in request.params.items() if 'ids[]' in k]
        else:
            response.content_type = "application/json"
            return '{"success": false}'

        nodes_json = []
        for id in id_list:
            node = Session.query(Node).filter(Node.id == id).first()
            nodes_json.append(node.__json__())

        csv = []
        if nodes_json:
            csv.append('\t'.join(nodes_json[0].keys()))
            csv_last = len(nodes_json[0].keys()) - 1
        else:
            response.content_type = "application/json"
            return '{"success": false}'

        for n in nodes_json:
            node_string = ''
            for i, val in enumerate(n.values()):
                if val == None:
                    val = ''

                if (i == csv_last):
                    node_string += '%s' % val
                else:
                    node_string += '%s\t' % val

            csv.append(node_string)

        response.content_type = "text/plain"
        response.headers['Content-disposition'] = \
            'attachment; filename=node_export.csv'
        return "\n".join(csv)

    @user_level(0)
    def create(self):
        data = {}
        data['hostname'] = request.params['hostname']
        data['service_tag'] = request.params['service_tag']
        data['primary_ip'] = request.params['primary_ip']
        data['location'] = request.params['location']
        data['description'] = request.params['description']

        activity_engine = ActivityEngine(Session,
                session['active_user']['user_id'])
        status = activity_engine.create('node', data)

        if status:
            session['flash'] = status['status']
            session.save()

        return redirect(url(controller='nodes',
            action='show', id=status['info']['id']))

    @user_level(0)
    def update(self, id, format='html'):
        ignore = ['Submit',
                'username']

        params = [
            (p, request.params[p]) for p in request.params \
                if p not in ignore]
        data = {}
        for key, value in params:
            if key == 'cpu_speed' and not value:
                continue
            elif key == 'game' and not value:
                continue
            data[key] = value

        activity_engine = ActivityEngine(Session,
                session['active_user']['user_id'])
        status = activity_engine.update('node', id, data)

        if format =='html':
            session['flash'] = status
            session.save()
            return redirect(url(controller='nodes', action='show', id=id))
        elif format == 'json':
            request.content_type = 'application/json'
            return status

    @user_level(0)
    def updatebyname(self, name, format='html'):
        id = Session.query(Node).filter(Node.hostname == name).first()
        if id:
            id = id.id
        else:
            return 'Host: %s is not in nodetraq' % name

        ignore = ['Submit',
                'username']

        params = [
            (p, request.params[p]) for p in request.params \
                if p not in ignore]
        data = {}
        for key, value in params:
            if value:
                if key == 'cpu_speed' and not value:
                    continue
                data[key] = value

        activity_engine = ActivityEngine(Session,
                session['active_user']['user_id'])
        status = activity_engine.update('node', id, data)

        if format =='html':
            session['flash'] = status
            session.save()
            return redirect(url(controller='nodes', action='show', id=id))
        elif format == 'json':
            request.content_type = 'application/json'
            return status

    @user_level(0)
    def updatemany(self):
        ignore = ['Submit', 'username']
        ids = []
        if 'ids[]' in request.params:
            for id in request.params['ids[]']:
                ids.append(id)

        data = {}
        for key, value in params:
            if key == 'cpu_speed' and not value:
                continue
            data[key] = value

        activity_engine = ActivityEngine(Session,
                session['active_user']['user_id'])

    @user_level(0)
    def addgroups(self):
        response.content_type = "application/json"
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        else:
            session['flash'] = 'No ids were sent'
            session.save()
            return '{"success": false}'

        data = {}
        data['add_groups'] = True

        if 'groups' in request.params:
            data['groups'] = [v for k,v in request.params.items()\
                                  if 'groups' in k]
        else:
            session['flash'] = 'No groups were sent'
            session.save()
            return '{"success": false}'
        activity_engine = ActivityEngine(
                Session, session['active_user']['user_id'])
        status = activity_engine.update_many('group', ids, data)

        session['flash'] = status
        session.save()
        return '{"success": true}'

    @user_level(0)
    def removegroups(self):
        response.content_type = "application/json"
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        else:
            session['flash'] = 'No ids were sent'
            session.save()
            return '{"success": false}'

        data = {}
        data['remove_groups'] = True
        if 'groups' in request.params:
            data['groups'] = [\
                    v for k,v in request.params.items() if 'groups' in k]
        else:
            session['flash'] = 'No groups were sent'
            session.save()
            return '{"success": false}'

        activity_engine = ActivityEngine(
                Session, session['active_user']['user_id'])
        status = activity_engine.update_many('group', ids, data)

        session['flash'] = status
        session.save()
        return '{"success": true}'

    @user_level(0)
    def addnagios(self):
        response.content_type = "application/json"
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        else:
            session['flash'] = 'No ids were sent'
            session.save()
            return '{"success": false}'

        data = {}
        data['add_nagios'] = True

        activity_engine = ActivityEngine(
                Session, session['active_user']['user_id'])
        status = activity_engine.update_many('group', ids, data)

        session['flash'] = status
        session.save()
        return '{"success": true}'

    @user_level(0)
    def removenagios(self):
        response.content_type = "application/json"
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items() if 'ids[]' in k]
        else:
            session['flash'] = 'No ids were sent'
            session.save()
            return '{"success": false}'

        data = {}
        data['remove_nagios'] = True

        activity_engine = ActivityEngine(
                Session, session['active_user']['user_id'])
        status = activity_engine.update_many('group', ids, data)

        session['flash'] = status
        session.save()
        return '{"sucess": true}'

    @user_level(0)
    def update_disks(self, hostname):
        response.content_type = "application/json"
        diskinfo = {'disks': []}
        if 'disks' in request.params:
            diskinfo['disks'] = json.loads(request.params['disks'])['disks']

        node = Session.query(Node).filter(Node.hostname == hostname).first()
        node.update_disks(diskinfo)
        return '{"success": true}'

    @user_level(0)
    def create_comment(self):
        content = None
        node = None
        if 'comment' in request.params:
            content = request.params['comment']
            if not content:
                return redirect(
                    url(controller='nodes', action='show', id=id))

            if 'node' in request.params:
                id = request.params['node']
                node = Session.query(Node)\
                    .filter(Node.id == id).first()

        if node:
            if not node.comments:
                node.comments = []
            comment = NodeComment()
            comment.node_id = id
            user = Session.query(User).filter(
                User.id == session['active_user']['user_id']).first()
            comment.user_id = session['active_user']['user_id']
            comment.description = content
            node.comments.append(comment)
            Session.add(node)
            Session.add(comment)
            Session.commit()

        return redirect(url(controller='nodes', action='show', id=id))

    @user_level(0)
    def edit_comment(self, id, commentid):
        c.title = 'Nodetraq : Comments'
        c.selected_page = 'nodes'
        c.subpage = 'editcomment'

        c.comment = Session.query(NodeComment)\
                .filter(NodeComment.id == commentid).first()
        c.node_id = id
        return render('/nodes/comments/edit.mako')

    @user_level(0)
    def update_comment(self, id, commentid):
        comment = Session.query(NodeComment)\
                .filter(NodeComment.id == commentid).first()
        if 'description' in request.params:
            comment.description = request.params['description']
        Session.add(comment)
        Session.commit()
        c.node_id = id
        return redirect(url(
            controller='nodes', action='show', id=id))

    @user_level(0)
    def destroy_comment(self, id, commentid):
        comment = Session.query(NodeComment)\
                .filter(NodeComment.id == commentid).first()
        Session.delete(comment)
        Session.commit()
        return redirect(url(
            controller='nodes', action='show', id=id))

    @user_level(0)
    def edit_flags(self):
        c.user = session['active_user']['username']
        c.flags = Session.query(Flag).all()
        return render('/nodes/flags/edit.mako')

    @user_level(0)
    def clear_flags(self):
        response.content_type = 'application/json'
        ids = None
        if 'ids[]' in request.params:
            ids = [v for k,v in request.params.items()\
                       if 'ids[]' in k]
        for node_id in ids:
            node = Session.query(Node).filter(
                Node.id == node_id).first()
            for count in xrange(len(node.flags)):
                del(node.flags[0])
            Session.add(node)
            Session.commit()

        session['flash'] = 'Flags were cleared'
        session.save()
        return '{"success": true}'

    @user_level(0)
    def update_flags(self):
        response.content_type = 'application/json'
        ids = None
        if 'ids[]' in request.params:
            ids = [int(v) for k,v in request.params.items()\
                       if 'ids[]' in k]
        else:
            session['flash'] = "No ids were passed"
            session.save()
            return '{"success": false}'

        flags = None
        if 'flags[]' in request.params:
            flags = [v for k,v in request.params.items()\
                         if 'flags[]' in k]
        else:
            session['flash'] = "No flags were passed"
            session.save()
            return '{"success": false}'

        description = None
        if 'description' in request.params:
            description = request.params['description']
        if 'user' in request.params:
            username = request.params['user']
        else:
            session['flash'] = "No username was passed"
            session.save()
            return '{"success": false"}'

        for node_id in ids:
            node = Session.query(Node).filter(
                Node.id == node_id).first()
            node.flags = []

            nfi = NodeFlagInfo()
            nfi.node = node
            nfi.user = Session.query(User).filter(
                User.name == username).first()
            nfi.description = description
            nfi.flags = Session.query(Flag)\
                                 .filter(Flag.name.in_(flags)).all()

            for f in ['setup', 'hardware', 'maintenance']:
                if f in flags:
                    comment = NodeComment()
                    comment.node_id = node.id
                    comment.user_id = nfi.user.id
                    comment.description = description
                    node.comments.append(comment)
                    Session.add(node)
                    Session.add(comment)
                    Session.commit()
                    break

            Session.add(nfi)
            Session.commit()

        session['flash'] = 'Flags were updated'
        session.save()
        return '{"success": true}'

    @user_level(0)
    def destroy(self, id):
        activity_engine = ActivityEngine(Session,
                session['active_user']['user_id'])
        status = activity_engine.destroy('node', id)

        if status:
            session['flash'] = 'Successfully %s' % status
            session.save()
        return redirect(url(controller='nodes', action='index'))

    @user_level(0)
    def batchedit(self):
        c.title = 'Nodetraq -- Batchedit'
        c.selected_page = 'nodes'
        c.subpage = 'batchedit'

        c.field = request.params['field']
        ids = None
        if 'ids[]' in request.params:
            ids = [int(v) for k,v in request.params.items()\
                       if 'ids[]' in k]
        if not ids:
            c.nodes = []
        else:
            c.nodes = [node for node in Session.query(Node)\
                           .filter(Node.id.in_(ids)).all()]

        return render('/nodes/batchedit/index.mako')

    @user_level(0)
    def sendbatchedit(self):
        response.content_type = 'application/json'
        user_id = int(request.params['user_id'])
        field = request.params['field']
        info = [json.loads(d[1]) for d in request.params.items()\
                    if 'items[]' in d]

        if field == 'hostname':
            for item in info:
                data = {}
                data['hostname'] = item['hostname']
                activity_engine = ActivityEngine(Session,
                        user_id)
                status = activity_engine.update(
                    'node', item['node_id'], data)
            session['flash'] = "Success"
            session.save()

        elif field == 'groups':
            for item in info:
                node = Session.query(Node)\
                    .filter(Node.id == item['node_id']).first()
                group_list = item['groups']\
                    .replace(' ', '').split(',')
                node.groups = Session.query(Group)\
                    .filter(Group.name.in_(group_list)).all()
                Session.add(node)
                Session.commit()
            session['flash'] = "Success"
            session.save()

        elif field == 'db_backups':
            for item in info:
                backup = Session.query(NodeDatabaseBackup)\
                    .filter(NodeDatabaseBackup.id == item['backup_id'])\
                    .first()
                node = Session.query(Node)\
                    .filter(Node.id == item['node_id']).first()
                backup.server_id = node.id

                if item['data_type'] == 'storage':
                    storage = Session.query(Node)\
                        .filter(Node.hostname == item['value']).first()
                    backup.storage_id = storage.id

                elif item['data_type'] == 'directory':
                    backup.directory = item['value']

            Session.add(backup)
            Session.commit()
            session['flash'] = "Success"
            session.save()
        else:
            return '{"success": false}'
        return '{"success": true}'

    @user_level(10)
    def show_dbbackups(self):
        c.title = "Nodetraq -- Show Database Backups"
        c.selected_page = "nodes"
        c.subpage = "database"
        sort = None

        c.dbbackups = Session.query(NodeDatabaseBackup).all()
        if not 'sort' in request.params:
            sort = 'server'
        else:
            sort = request.params['sort']

        if sort == 'server':
            c.dbbackups = sorted(
                c.dbbackups, key=lambda backup: backup.server.hostname)
        elif sort == 'storage':
            c.dbbackups = sorted(
                c.dbbackups, key=lambda backup: backup.storage.hostname)
        elif sort == 'directory':
            c.dbbackups = sorted(
                c.dbbackups, key=lambda backup: backup.directory)
        elif sort == 'enabled':
            c.dbbackups = sorted(
                c.dbbackups, key=lambda backup: backup.enabled)

        c.sort = sort

        return render('/nodes/show_dbbackups.mako')

    @user_level(0)
    def edit_bulk_dbbackups(self):
        c.title = "Nodetraq -- Edit Database Backups"
        c.selected_page = "nodes"
        c.subpage = "database"

        c.dbbackups = Session.query(NodeDatabaseBackup).all()
        c.dbbackups = sorted(
            c.dbbackups, key=lambda backup: backup.server.hostname)
        return render('/nodes/edit_bulk_dbbackups.mako')

    @user_level(0)
    def show_studio(self, id):
        c.studio = Session.query(Studio).filter(Studio.id == id).first()
        c.title = "Nodetraq -- Studio: %s" % c.studio.name
        c.header = c.studio.name
        c.selected_page = "nodes"
        c.subpage = "show_studio"

        c.groups = [
            {'name': 'PE-1950', 'nodes': []},
            {'name': 'PE-2950', 'nodes': []},
            {'name': 'PE-R410', 'nodes': []},
            {'name': 'PE-R610', 'nodes': []},
            {'name': 'PE-R710', 'nodes': []},
            {'name': 'vm', 'nodes': []},
            {'name': 'unknown', 'nodes': []}
            ]

        group_list = lambda groups: [g.name for g in groups]
        for game in c.studio.games:
            for node in game.nodes:
                grouped = False
                for group in c.groups:
                    if group['name'] in group_list(node.groups):
                        group['nodes'].append(node)
                        grouped = True

            if not grouped:
                c.groups[len(c.groups)-1]['nodes'].append(node)

        return render('/nodes/studios/show.mako')

    @user_level(0)
    def create_studio(self):
        c.title = "Nodetraq -- Create Studio"
        c.header = "Create Studio"
        c.selected_page = "nodes"
        c.subpage = "create_studio"
        return render('/nodes/studios/create.mako')

    @user_level(0)
    def edit_studio(self, id):
        c.studio = Session.query(Studio).filter(Studio.id == id).first()
        c.title = "Nodetraq -- Edit Studio"
        c.header = c.studio.name
        c.selected_page = "nodes"
        c.subpage = "edit_studio"
        return render('/nodes/studios/edit.mako')

    @user_level(0)
    def list_studios(self):
        c.studios = Session.query(Studio).all()
        c.title = "Nodetraq List Studios"
        c.selected_page = "nodes"
        c.subpage = "list_studios"
        return render('/nodes/studios/list.mako')

    @user_level(0)
    @jsonify
    def new_studio(self):
        params = json.loads(request.params.iteritems().next()[0])
        studio = Studio()
        studio.name = params['name']
        if 'description' in params:
            studio.description = params['description']
        Session.add(studio)
        Session.commit()

        session['flash'] = "Success"
        session.save()
        return {'success': True}

    @user_level(0)
    @jsonify
    def destroy_studio(self, id):
        studio = Session.query(Studio).filter(Studio.id == id).first()
        Session.delete(studio)
        Session.commit()

        session['flash'] = "Success"
        session.save()
        return {'success': True}

    @user_level(0)
    @jsonify
    def update_studio(self, id):
        studio = Session.query(Studio).filter(Studio.id == id).first()
        studio.name = request.params['name']
        if 'description' in request.params:
            studio.description = request.params['description']

        Session.add(studio)
        Session.commit()

        session['flash'] = "Success"
        session.save()
        return {'success': True}

    @user_level(0)
    @jsonify
    def batch_update_studios(self):
        for key in request.params:
            key = json.loads(key)
            nodes = key['ids']
            studio = key['studio']
            break

        nodes = Session.query(Node).filter(Node.id.in_(nodes)).all()
        studio = Session.query(Studio).filter(Studio.id == studio).first()

        for node in nodes:
            node.studio = studio
            Session.add(node)

        Session.commit()
        return {'success': True}

    @user_level(0)
    def show_game(self, id):
        c.game = Session.query(Game).filter(Game.id == id).first()
        c.title = "Nodetraq -- Game: %s" % c.game.name
        c.header = c.game.name
        c.selected_page = "nodes"
        c.subpage = "show_game"

        c.groups = [
            {'name': 'PE-1950', 'nodes': []},
            {'name': 'PE-2950', 'nodes': []},
            {'name': 'PE-R410', 'nodes': []},
            {'name': 'PE-R610', 'nodes': []},
            {'name': 'PE-R710', 'nodes': []},
            {'name': 'vm', 'nodes': []},
            {'name': 'unknown', 'nodes': []}
            ]

        group_list = lambda groups: [g.name for g in groups]
        for node in c.game.nodes:
            grouped = False
            for group in c.groups:
                if group['name'] in group_list(node.groups):
                    group['nodes'].append(node)
                    grouped = True

            if not grouped:
                c.groups[len(c.groups)-1]['nodes'].append(node)

        return render('/nodes/games/show.mako')

    @user_level(0)
    def create_game(self):
        c.title = "Nodetraq -- Create Game"
        c.header = "Create Game"
        c.selected_page = "nodes"
        c.subpage = "create_game"
        c.studios = [ ('', '') ]
        for studio in Session.query(Studio).all():
            c.studios.append((studio.id, studio.name))
        return render('/nodes/games/create.mako')

    @user_level(0)
    def edit_game(self, id):
        c.game = Session.query(Game).filter(Game.id == id).first()
        c.title = "Nodetraq -- Edit Game"
        c.header = c.game.name
        c.selected_page = "nodes"
        c.subpage = "edit_game"
        c.studio_list = [ ('', '') ]
        for studio in Session.query(Studio).all():
            c.studio_list.append((studio.id, studio.name))

        c.selected_studio = 0
        if c.game.studio:
            for studio in c.studio_list:
                if studio[1] == c.game.studio.name:
                    c.selected_studio = studio[0]
                    break
        return render('/nodes/games/edit.mako')

    @user_level(0)
    def list_games(self):
        c.games = Session.query(Game).all()
        c.title = "Nodetraq List Games"
        c.selected_page = "nodes"
        c.subpage = "list_games"
        return render('/nodes/games/list.mako')

    @user_level(0)
    @jsonify
    def new_game(self):
        game = Game()
        params = json.loads(request.params.iteritems().next()[0])
        game.name = params['name']
        if 'description' in params:
            game.description = params['description']
        if 'studio' in params:
            game.studio = Session.query(Studio).filter(
                Studio.id == params['studio']).first()
        Session.add(game)
        Session.commit()

        session['flash'] = "Success"
        session.save()
        return {'success': True}

    @user_level(0)
    @jsonify
    def destroy_game(self, id):
        game = Session.query(Game).filter(Game.id == id).first()
        Session.delete(game)
        Session.commit()

        session['flash'] = "Success"
        session.save()
        return {'success': True}

    @user_level(0)
    @jsonify
    def update_game(self, id):
        game = Session.query(Game).filter(Game.id == id).first()
        game.name = request.params['name']
        if 'description' in request.params:
            game.description = request.params['description']
        if 'studio' in request.params:
            game.studio = Session.query(Studio).filter(
                Studio.id == int(request.params['studio'])).first()

        Session.add(game)
        Session.commit()

        session['flash'] = "Success"
        session.save()
        return {'success': True}

    @user_level(0)
    @jsonify
    def batch_update_games(self):
        for key in request.params:
            key = json.loads(key)
            nodes = key['ids']
            game = key['game']
            break

        nodes = Session.query(Node).filter(Node.id.in_(nodes)).all()
        game = Session.query(Game).filter(Game.id == game).first()

        for node in nodes:
            node.game = game
            Session.add(node)

        Session.commit()
        return {'success': True}

