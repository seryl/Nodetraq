import logging
import json

from sqlalchemy.schema import CreateTable

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.model.meta import Session, now
from nodetraq.model.nodes import Node, NodeDatabaseBackup, BackupType
from nodetraq.lib.emailhelper import send_email
from pylons.decorators import jsonify

log = logging.getLogger(__name__)

class DbbackupsController(BaseController):

    @user_level(0)
    def index(self, id):
        c.title = 'Nodetraq - dbbackups'
        c.selected_page = 'nodes'
        c.subpage = 'dbbackups'
        c.header = 'Nodes : Db backups'

        c.node = Session.query(Node).filter(Node.id == id).first()
        c.node_id = c.node.id

        return render('/nodes/dbbackups/index.mako')

    @user_level(0)
    def new(self, id):
        c.title = 'Nodetraq - dbbackups'
        c.selected_page = 'nodes'
        c.subpage = 'dbbackups'
        c.header = 'Nodes : Db backups'
        c.node_id = id

        c.backup_type_list = [(t.id, t.name) for t in
                              Session.query(BackupType).all()]

        return render('/nodes/dbbackups/new.mako')

    @user_level(0)
    def edit(self, id, backup_id):
        c.title = 'Nodetraq - dbbackups'
        c.selected_page = 'nodes'
        c.subpage = 'dbbackups'
        c.header = 'Nodes : Db backups'
        c.node_id = id
        c.node_backup = Session.query(NodeDatabaseBackup).filter(
            NodeDatabaseBackup.id == backup_id).first()
        c.backup_id = backup_id

        c.backup_type_list = [(t.id, t.name) for t in
                              Session.query(BackupType).all()]

        return render('/nodes/dbbackups/edit.mako')

    @user_level(0)
    def create(self, id):
        node = Session.query(Node).filter(Node.id == id).first()
        if not node.db_backups:
            node.db_backups = []

        node_backup = NodeDatabaseBackup()
        node_backup.enabled = True
        node_backup.server = Session.query(Node)\
                .filter(Node.id == id).first()
        node_backup.server_id = node_backup.server.id
        node_backup.storage = Session.query(Node)\
                .filter(Node.hostname == \
                request.params['storage']).first()
        node_backup.storage_id = node_backup.storage.id
        node_backup.directory = request.params['directory']
        node_backup.backup_type_id = request.params['backup_type']

        if node_backup.storage and node_backup.server:
            Session.add(node_backup)
            Session.commit()
            node.db_backups.append(node_backup)
            Session.add(node)
            Session.commit()
        else:
            session['flash'] = 'Storage hostname doesn\'t exist'
            session.save()

        return redirect(url(controller='dbbackups', action='index', id=id))

    @user_level(0)
    def update(self, id, backup_id):
        for k,v in request.params.iteritems():
            params = json.loads(k)
            break
        storage = params['storage']
        directory = params['directory']
        enabled = params['enabled']
        backup_type_id = params['backup_type']
        node_backup = Session.query(NodeDatabaseBackup).filter(
            NodeDatabaseBackup.id == backup_id).first()
        node_backup.server = Session.query(Node)\
                .filter(Node.id == id).first()
        node_backup.server_id = node_backup.server.id
        node_backup.storage = Session.query(Node)\
                .filter(Node.hostname == \
                storage).first()
        node_backup.storage_id = node_backup.storage.id
        node_backup.directory = directory
        node_backup.enabled = enabled
        node_backup.backup_type_id = backup_type_id

        if node_backup.storage and node_backup.server:
            Session.add(node_backup)
            Session.commit()
        else:
            session['flash'] = 'Storage hostname doesn\'t exist'
            session.save()

        return redirect(url(controller='dbbackups', action='index', id=id))

    @user_level(10)
    @jsonify
    def enable(self, id, backup_id):
        node_backup = Session.query(NodeDatabaseBackup).filter(
            NodeDatabaseBackup.id == backup_id).first()
        node_backup.enabled = True
        Session.add(node_backup)
        Session.commit()

        c.backup_server = node_backup.server.hostname
        c.backup_type = node_backup.backup_type.name
        c.backup_storage = node_backup.storage.hostname
        c.backup_directory = node_backup.directory
        if session['active_user']:
            c.user = session['active_user']['username']

        send_email(
            render('/email/backups/enable.mako'),
            'Enabled backup: %s' % c.backup_server,
            email_from='admin@yourdomain',
            email_to=['email_user@yourdomain'])
        return {"success": True}

    @user_level(10)
    @jsonify
    def disable(self, id, backup_id):
        node_backup = Session.query(NodeDatabaseBackup).filter(
            NodeDatabaseBackup.id == backup_id).first()
        node_backup.enabled = False
        Session.add(node_backup)
        Session.commit()

        c.backup_server = node_backup.server.hostname
        c.backup_type = node_backup.backup_type.name
        c.backup_storage = node_backup.storage.hostname
        c.backup_directory = node_backup.directory
        if session['active_user']:
            c.user = session['active_user']['username']

        send_email(
            render('/email/backups/disable.mako'),
            'Disabled backup: %s' % c.backup_server,
            email_from='admin@yourdomain',
            email_to=['email_user@yourdomain'])
        return {"success": True}

    @user_level(0)
    def destroy(self, id, backup_id):
        dbbackup = Session.query(NodeDatabaseBackup)\
            .filter(NodeDatabaseBackup.id == backup_id).first()
        Session.delete(dbbackup)
        Session.commit()
        session['flash'] = "Successfully destroyed dbbackup"
        session.save()

        return redirect(url(controller='dbbackups', action='index', id=id))

    @user_level(0)
    @jsonify
    def delete(self, backup_id):
        dbbackup = Session.query(NodeDatabaseBackup)\
            .filter(NodeDatabaseBackup.id == backup_id).first()
        Session.delete(dbbackup)
        Session.commit()
        return {"success": True}

    @user_level(0)
    @jsonify
    def bulk_update(self):
        for k,v in request.params.iteritems():
            data = json.loads(k)
            # updates
            for update in data['updates']:
                try:
                    node_backup = Session.query(NodeDatabaseBackup).filter(
                        NodeDatabaseBackup.id == update['id']).first()
                    node_backup.server = Session.query(Node)\
                        .filter(Node.hostname == update['server']).first()
                    node_backup.server_id = node_backup.server.id
                    node_backup.storage = Session.query(Node)\
                        .filter(Node.hostname == \
                                    update['storage']).first()
                    node_backup.storage_id = node_backup.storage.id
                    node_backup.directory = update['directory']
                    node_backup.enabled = update['enabled']

                    if node_backup.storage and node_backup.server:
                        Session.add(node_backup)
                        Session.commit()
                except Exception as e:
                    session['flash'] = "Error: %s" % e
                    session.save()
                    return {"success": False}

            # new backups
            for backup in data['new_backups']:
                try:
                    node = Session.query(Node).filter(
                        Node.hostname == backup['server']).first()
                    if not node.db_backups:
                        node.db_backups = []

                    node_backup = NodeDatabaseBackup()
                    node_backup.enabled = backup['enabled']
                    node_backup.server = node
                    node_backup.server_id = node_backup.server.id
                    node_backup.storage = Session.query(Node)\
                        .filter(Node.hostname == \
                                    backup['storage']).first()
                    node_backup.storage_id = node_backup.storage.id
                    node_backup.directory = backup['directory']

                    if node_backup.storage and node_backup.server:
                        Session.add(node_backup)
                        Session.commit()
                        node.db_backups.append(node_backup)
                        Session.add(node)
                        Session.commit()
                except Exception as e:
                    session['flash'] = "Error: %s" % e
                    session.save()
                    return {"success": False}

        session['flash'] = "Successfully updated backups!"
        session.save()
        return {"success": True}
