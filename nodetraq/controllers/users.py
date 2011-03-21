import logging
import re
import json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from nodetraq.model.meta import Session

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.lib.directoryhelper import DirectoryHelper
from nodetraq.lib.activity import ActivityEngine

from ldap import modlist as modlist

log = logging.getLogger(__name__)

directoryCN = 'manage_cn'
directoryPassword = 'your_manager_password'
directoryDomain = 'yourdirectorydomain'

class UsersController(BaseController):
    @user_level(0)
    def __before__(self):
        super(UsersController, self).__before__()

    def index(self):
        c.title = "Nodetraq -- Users"
        c.selected_page = "users"
        c.subpage = "index"

        sort_type = None
        if request.params.has_key('sort'):
            sort_type = request.params['sort']

        sort_order = None
        if request.params.has_key('order'):
            sort_order = request.params['order']

        if sort_type == None:
            c.sort_type = 'givenName'
        else:
            c.sort_type = sort_type

        if sort_order == None:
            c.sort_order = 'asc'
        else:
            c.sort_order = sort_order

        if sort_order == 'asc':
            sort_order = False
        else:
            sort_order = True

        c.search_type = None
        if request.params.has_key('search_type'):
            c.search_type = request.params['search_type']

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)

        users = None
        if 'search_field' in request.params:
            if request.params['search_field']:
                fltr = \
                    '(&(objectClass=person)(uid=*%s*)(!(objectClass=computer)))' % \
                    request.params['search_field']
            else: fltr = '(&(objectClass=person)(!(objectClass=computer)))'
            users = dh.ldap.search(
                Filter=fltr,
                Attrs=['*', 'nsAccountLock'])
        if not users:
            users = dh.ldap.search(BaseDN='ou=People,DC=yourdomain,DC=com',
                Filter='(&(objectClass=person)(!(objectClass=computer)))',
                Attrs=['*', 'nsAccountLock'])

        restricted = (
            ['Administrator'], ['Guest'], ['DHCP_Registrations'])
        c.users = [u for u in users if u[0]]
        c.users = [u for u in c.users if not u[1]['givenName'] in restricted]
        for user in c.users:
            if not user[1].has_key('mail'):
                user[1]['mail'] = ['']
            if not user[1].has_key('uidNumber'):
                user[1]['uidNumber'] = ['']

        c.users = [u for u in c.users]
        if sort_type == None:
            #print c.users
            enabled_users = [u for u in c.users if u[1]['nsAccountLock'][0].lower() == 'false']
            enabled_users = sorted(enabled_users,
                                   key = lambda user: user[1]['uid'],
                                   reverse=False)

            disabled_users = [u for u in c.users if u[1]['nsAccountLock'][0].lower() == 'true']
            disabled_users = sorted(disabled_users,
                                    key = lambda user: user[1]['uid'],
                                    reverse=False)
            c.users = enabled_users + disabled_users
        else:
            c.users = sorted(c.users,
                             key=lambda user: user[1][sort_type],
                             reverse=sort_order)
        return render('/users/index.mako')

    def groups(self):
        c.title = "Nodetraq -- Ldap Search"
        c.selected_page = "users"
        c.subpage = "list"

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        data = dh.ldap.search_groups()
        data = [d for d in data if d[0]]
        c.users = data
        sort_type = 'cn'
        if request.params.has_key('sort'):
            sort_type = request.params['sort']

        sort_order = 'asc'
        if request.params.has_key('order'):
            sort_order = request.params['order']

        c.sort_type = sort_type
        c.sort_order = sort_order

        if sort_order == 'asc':
            sort_order = False
        else:
            sort_order = True

        c.search_type = None
        if request.params.has_key('search_type'):
            c.search_type = request.params['search_type']

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        if 'search_field' in request.params:
            if request.params['search_field']:
                fltr = \
                    '(&(objectClass=groupofuniquenames)(cn=*%s*))' % \
                    request.params['search_field']
            else:
                fltr = '(&(objectClass=groupofuniquenames))'
            data = dh.ldap.search_groups(
                Filter=fltr,
                Attrs=['cn', 'description'])
        else:
            data = dh.ldap.search_groups(Attrs=['cn', 'description'])
        for item in data:
            if not item[1].has_key('description'):
                item[1]['description'] = ['']

        c.groups = data
        c.groups = sorted(c.groups,
                          key=lambda group: group[1][sort_type],
                          reverse=sort_order)

        return render('/users/groups.mako')

    def new(self):
        c.title = "Nodetraq -- Create"
        c.selected_page = "users"
        c.subpage = "create"

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        c.available_groups = dh.ldap.search_groups(
            Attrs=['cn', 'description'])
        c.available_groups = [g[1]['cn'][0] for g in c.available_groups]
        c.available_groups = sorted(c.available_groups,
                                    key=lambda group: group)

        c.groups = []
        return render('/users/new.mako')

    def newgroup(self):
        c.title = "Nodetraq -- Create Group"
        c.selected_page = "users"
        c.subpage = "creategroup"
        return render('/users/newgroup.mako')

    def create(self):
        hash_params = ('username', 'name', 'mail',
                       'loginShell', 'title', 'manager',
                       'departmentNumber', 'roomNumber',
                       'orgchartmanager', 'utilityaccount', 'deploycode')
        dh = DirectoryHelper(
                directoryCN, directoryPassword, directoryDomain)

        data_map = {}
        groups = []
        for k,v in request.params.items():
            if k in hash_params:
                data_map[k] = v
            elif k == 'group':
                groups.append(v)

        data_map['username'] = data_map['username'].lower()

        dh.ldap.create(data_map['username'], data_map['name'],
                       data_map['mail'], data_map['loginShell'],
                       data_map['title'], data_map['manager'],
                       data_map['departmentNumber'], data_map['roomNumber'],
                       data_map['deploycode'], data_map['orgchartmanager'],
                       data_map['utilityaccount'] )

        dh.set_groups(data_map['username'], groups)

        session['flash'] = 'Successfully created %s' % data_map['username']
        session.save()

        data_map['account'] = data_map['username']
        ae = ActivityEngine(Session, session['active_user']['user_id'])
        ae.create('user', data_map)

        return redirect(url(
                controller='users', action='edit',
                account=data_map['username']))

    def creategroup(self):
        name = None
        if 'name' in request.params:
            name = request.params['name']

        description = None
        if 'description' in request.params:
            description = request.params['description']

        try:
            dh = DirectoryHelper(
                directoryCN, directoryPassword, directoryDomain)
            dh.ldap.create_group(name, description)

            session['flash'] = 'Successfully created group %s' % name
            session.save()
        except:
            session['flash'] = 'Group %s already exists' % name
            session.save()
        return redirect(url(
                controller='users', action='groups'))

    def updategroup(self, group):
        cn = None
        if 'cn' in request.params:
            cn = request.params['cn']
        description = None
        if 'description' in request.params:
            description = request.params['description']

        try:
            dh = DirectoryHelper(
                directoryCN, directoryPassword, directoryDomain)
            group_dn = 'cn=%s,ou=groups,dc=yourdomain,dc=com' % group
            if cn != group:
                dh.update_dn(group_dn, 'cn=%s' % cn)
            dh.update_group_attribute(cn, 'description', description)
            dh.update_group_attribute(cn, 'cn', cn)
        except:
            pass
        session['flash'] = 'Successfully updated group'
        session.save()
        return redirect(url(
                controller='users', action='editgroup', group=cn))

    def search(self):
        c.title = "Nodetraq -- Search"
        c.selected_page = "users"
        c.subpage = "search"

        c.search_type = 'users'
        return render('/users/search.mako')

    def edit(self, account=None):
        c.title = "Nodetraq -- Edit Users"
        c.selected_page = "users"
        c.subpage = "edit"

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        try:
            c.user = dh.ldap.findUser(account, Attrs=[
                    'cn', 'uid',
                    'mail', 'loginShell', 'nsAccountLock',
                    'uidNumber', 'title', 'manager',
                    'departmentNumber', 'roomNumber',
                    'deploycode', 'orgchartmanager', 'utilityaccount'
                    ])[1]
            fix_keys = ['uidNumber', 'nsAccountLock',
                        'mail', 'loginShell']
            for key in fix_keys:
                if not c.user.has_key(key):
                    c.user[key] = ['']
        except:
            c.user = None
        groups = dh.getAllGroups()
        c.group_membership = dh.getUserGroups(account)
        c.group_membership.sort()
        c.available_groups = list(set(groups) - set(c.group_membership))
        c.available_groups.sort()
        return render('/users/edit.mako')

    def editgroup(self, group=None):
        c.title = "Nodetraq -- Edit User Groups"
        c.selected_page = "users"
        c.subpage = "edit"

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        try:
            c.group = dh.ldap.search(
                Filter='cn=%s' % group,
                Attrs=['cn', 'description'])[0][1]
        except:
            c.group = None

        return render('/users/editgroup.mako')

    def group_members(Self, group=None):
        c.title = "Nodetraq -- Group Members - %s" % group
        c.selected_page = "users"
        c.subpage = "members"

        sort_type = 'uid'
        if request.params.has_key('sort'):
            sort_type = request.params['sort']

        sort_order = 'asc'
        if request.params.has_key('order'):
            sort_order = request.params['order']

        c.sort_type = sort_type
        c.sort_order = sort_order

        if sort_order == 'asc':
            sort_order = False
        else:
            sort_order = True

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)

        c.group = group

        try:
            c.members = dh.ldap.show_group_members(group)
            c.members = [dh.ldap.findUser(m) for m in c.members]
            c.members = [m for m in c.members if m]
            c.members = [m for m in c.members if m[1].has_key(sort_type)]
            c.members = sorted(c.members,
                               key=lambda member: member[1][sort_type],
                               reverse=sort_order)
        except Exception as e:
            print e
            c.members = []

        return render('/users/group_members.mako')

    def remove_members(self, group):
        members = []
        for k in request.params:
            members = json.loads(k)['members']
            break

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)

        for member in members:
            dh.remove_group(member, group)

        session['flash'] = 'Successfully updated %s' % group
        session.save()

    def update(self, account):
        update_items = (
            'cn', 'uidNumber', 'mail',
            'loginShell', 'title', 'manager',
            'departmentNumber', 'roomNumber',
            'deploycode', 'orgchartmanager', 'utilityaccount')

        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)

        updates = {}
        groups = [v for k,v in request.params.items() if k == 'group']
        for item in update_items:
            if item in request.params:
                if item == 'cn':
                    updates['cn'] = request.params[item]
                    updates['gecos'] = request.params[item]
                    splitname = request.params[item].split()
                    updates['givenName'] = splitname[0]
                    if len(splitname) > 1:
                        updates['sn'] = splitname[1]
                updates[item] = request.params[item]

        # for key in updates, update ldap and ad
        for k, v in updates.iteritems():
            dh.update_attribute(account, k, v)
        # for group in groups, update ldap groups
        dh.set_groups(account, groups)

        session['flash'] = 'Successfully updated %s' % account
        session.save()

        updates['account'] = account
        ae = ActivityEngine(Session, session['active_user']['user_id'])
        ae.update('user', None, updates)

        return redirect(url(controller='users', action='edit', account=account))

    def change_password(self, account):
        if 'password' in request.params:
            password = request.params['password']

            dh = DirectoryHelper(
                directoryCN, directoryPassword, directoryDomain)
            dh.change_password(account, password)

            session['flash'] = "Password changed successfully"
            session.save()
            return redirect(url(
                    controller='users', action='edit', account=account))

        session['flash'] = "Error changing password"
        session.save()
        return redirect(url(
                controller='users', action='edit', account=account))

    def reset_password(self, account):
        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        result = dh.reset_password(account)

        if result:
            session['flash'] = 'Reset password successfully'
            session.save()
            # Mail reset password
        else:
            session['flash'] = 'Error resetting password'
            session.save()
        return redirect(url(controller='users', action='edit', account=account))

    def rename_user(self, account):
        c.account = account
        return render('/users/rename_user.mako')

    def rename_user_service(self, account):
        if 'new_username' in request.params:
            new_username = request.params['new_username']
            if new_username:
                # rename user here
                session['flash'] = 'Renamed %s to %s successfully' % (
                    account, new_username)
                session.save()
                return redirect(url(
                        controller='users', action='edit', account=new_username))

        session['flash'] = 'Error renaming %s' % account
        session.save()
        return redirect(url(
                controller='users', action='edit', account=account))

    def disable_user(self, account):
        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        result = dh.disable_user(account)

        if result:
            session['flash'] = 'Successfully disabled %s' % account
            session.save()
        else:
            session['flash'] = 'Error disabling %s' % account
            session.save()

        ae = ActivityEngine(Session, session['active_user']['user_id'])
        ae.update('user', None,
                  { 'nsAccountLock': 'true', 'account': account })

        return redirect(url(
                controller='users', action='edit', account=account))

    def enable_user(self, account):
        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        result = dh.enable_user(account)
        if result:
            session['flash'] = 'Successfully enabled %s' % account
            session.save()
        else:
            session['flash'] = 'Error disabling %s' % account
            session.save()

        ae = ActivityEngine(Session, session['active_user']['user_id'])
        ae.update('user', None,
                  { 'nsAccountLock': 'false', 'account': account })

        return redirect(url(
                controller='users', action='edit', account=account))

    def delete_user(self, account):
        dh = DirectoryHelper(
            directoryCN, directoryPassword, directoryDomain)
        session['flash'] = 'Successfully deleted %s' % account
        session.save()
        return redirect(url(
                controller='users', action='index'))

