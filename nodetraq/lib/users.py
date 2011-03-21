import ldap, ldap.ldapobject
import ldap.modlist as modlist

import base64
import string
from hashlib import sha1
from random import choice

from nodetraq.model.meta import Session
from nodetraq.model.users import User, _ldap_server, _ldap_server2, \
    _baseDN, _ops_dn
from pylons import tmpl_context as c
from nodetraq.lib.base import render
from emailhelper import send_email
from sshwrapper import run_ssh_command
from activity import ActivityEngine

def GeneratePassword(length):
    "Generates a random password with the given length."
    return ''.join([
        choice(string.letters+string.digits)\
                for i in xrange(0, length)])

class ActiveDirectory(object):
    def __init__(self, server=None, username=None,
                 password=None, domain=None):
        self.connection = ldap.ldapobject.LDAPObject(server)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
        self.connection.set_option(ldap.OPT_REFERRALS, 0)
        self.connection.simple_bind_s(
            '@'.join([username, domain]), password)

    def search(self, BaseDN='DC=yourdomain,DC=com',
               Scope=ldap.SCOPE_SUBTREE,
               Filter="(&(objectClass=user))",
               Attrs=None):

        s = self.connection.search(
            BaseDN, Scope, Filter, Attrs)
        result = self.connection.result(s, 60)
        return result[1]

    def search_users(self,
                     Filter="(&(objectClass=user)(!(objectClass=computer)))",
                     Attrs=None):
        BaseDN='DC=yourdomain,DC=com'
        return self.search(BaseDN, Filter=Filter, Attrs=Attrs)

    def search_groups(self, Filter="(&(objectClass=groupofuniquenames))",
                      Attrs=None):
        BaseDN='OU=Groups,DC=yourdomain,DC=com'
        return self.search(BaseDN, Filter=Filter, Attrs=Attrs)

    def update_attribute(self, dn, attr, values,
                         mode=ldap.MOD_REPLACE):
        self.connection.modify_s(
            dn, [(mode, attr, values)])
        return True

    def update_password(self, username, password):
        userDN = self.findUser(username)[0]
        if not userDN:
            return False
        new_password = ('"%s"' % password).encodestring("utf-16-le")
        return self.update_attribute(
            userDN, 'unicodePwd', new_password)

    def create(self, username, full_name, email, shell='/bin/bash'):
        attrs = {}
        attrs['distinguishedName'] = \
            'cn=%s,ou=users,ou=\\+Objects,dc=yourdomain,dc=com' % full_name
        attrs['objectClass'] = [
            'top', 'posixAccount',
            'person', 'organizationalPerson',
            'user', 'account']
        attrs['primaryGroup'] = '513'
        attrs['sAMAccountName'] = username
        attrs['uid'] = username
        attrs['cn'] = full_name
        attrs['givenName'] = full_name.split()[0]
        attrs['sn'] = full_name.split()[1]
        attrs['mail'] = email
        attrs['homeDirectory'] = '/home/%s' % username
        attrs['objectCategory'] = [
            'cn=person,cn=schema,cn=configuration,dc=yourdomain,dc=com']
        attrs['loginShell'] = shell
        attrs['instanceType'] = '4'
        attrs['countryCode'] = '0'
        attrs['userAccountControl'] = '544'
        attrs['gidNumber'] = '1008'
        # Note: 544 = enabled, 546 = disabled

        ldif = modlist.addModlist(attrs)
        userDN = 'cn=%s,ou=users,ou=\\+Objects,dc=yourdomain,dc=com' \
            % full_name
        self.connection.add_s(userDN, ldif)

    def disableUser(self, username):
        dn = findUser(username)[0]
        if not dn:
            return False
        self.update_attribute(dn, 'userAccountControl', '546')
        return True

    def findUser(self, username, use_name=False, Attrs=None):
        if use_name:
            try:
                user_data = self.search(
                    Filter='name=%s' % (username),
                    Attrs=Attrs)[0]
            except:
                return None
        else:
            try:
                user_data = self.search(
                    Filter='sAMAccountName=%s' % (username),
                    Attrs=Attrs)[0]
            except:
                return None

        if not user_data[0]:
            return None
        return user_data

    def deleteUser(self, userDN):
        self.connection.delete(userDN)

class LdapDirectory(object):
    def __init__(self, server=None, username=None,
                 password=None, domain=None):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, False)
        self.connection = ldap.ldapobject.LDAPObject(server)
        if not username.startswith('cn='):
            usernameDN = 'uid='+username+','+_baseDN
        else:
            usernameDN = username
        self.connection.simple_bind_s(usernameDN, password)

    def search(self, BaseDN='DC=yourdomain,DC=com',
               Scope=ldap.SCOPE_SUBTREE, Filter=\
                   '(|(objectClass=person)(objectClass=groupofuniquenames))',
               Attrs=None):
        s = self.connection.search(
            BaseDN, Scope, Filter, Attrs)
        result = self.connection.result(s, 60)
        return result[1]

    def search_users(self, Filter="(&(objectClass=person))",
                     Attrs=None):
        BaseDN='OU=People,DC=yourdomain,DC=com'
        return self.search(BaseDN, Filter=Filter, Attrs=Attrs)

    def search_groups(self, Filter="(&(objectClass=groupofuniquenames))",
                      Attrs=None):
        BaseDN='OU=Groups,DC=yourdomain,DC=com'
        return self.search(BaseDN, Filter=Filter, Attrs=Attrs)

    def show_group_members(self, group, Attrs=['uniqueMember']):
        BaseDN='OU=Groups,DC=yourdomain,DC=com'
        Filter="(&(objectClass=groupofuniquenames)(cn=%s))" % group
        memberlist = self.search(BaseDN, Filter=Filter, Attrs=Attrs)
        if memberlist:
            memberlist = memberlist[0][1]
            memberlist = [''.join(m.split()) for m in \
                              memberlist['uniqueMember']]
            memberlist = [m.split(',')[0] for m in \
                              memberlist]
            memberlist = [m.split('=')[1] for m in \
                              memberlist]
        return memberlist

    def update_attribute(self, dn, attr, values,
                         mode=ldap.MOD_REPLACE):
        if isinstance(values, unicode):
            self.connection.modify_s(
                dn, [(mode, attr, str(values))])
        else:
            self.connection.modify_s(
                dn, [(mode, attr, values)])
        return True

    def update_dn(self, dn, new_dn):
        self.connection.modrdn_s(dn, new_dn, True)
        return True

    def disable_user(self, username):
        userDN = self.findUser(username)[0]
        if not userDN:
            return False
        new_password = GeneratePassword(10)
        self.update_password(username, new_password)
        return self.update_attribute(
                userDN, 'nsAccountLock', 'true')

    def enable_user(self, username):
        userDN = self.findUser(username)[0]
        if not userDN:
            return False
        return self.update_attribute(
                userDN, 'nsAccountLock', 'false')

    def update_password(self, username, password):
        userDN = self.findUser(username)[0]
        if not userDN:
            return False
        new_password = self._makepasswd(password)
        return self.update_attribute(
                userDN, 'userPassword', new_password)

    def reset_password(self, username):
        userInfo = self.findUser(username)
        userDN = userInfo[0]
        if not userDN:
            return False
        new_password = GeneratePassword(10)

        c.new_account = False
        c.username = userInfo[1]['uid'][0]
        c.password = new_password

        if self.update_attribute(
                userDN, 'userPassword', new_password):
            send_email(render('email/ldap_account.mako'),
                'Password reset request', email_to=userInfo[1]['mail'])
            return new_password
        else:
            return None

    def create(self, username, full_name, email, shell='/bin/bash',
               title='', manager='',
               departmentNumber='', roomNumber='',
               deploycode = 'false', orgchartmanager = 'false',
               utilityaccount = 'false'):
        username = str(username)
        full_name = str(full_name)
        email = str(email)
        shell = str(shell)
        title = str(title)
        manager = str(manager)
        departmentNumber = str(departmentNumber)
        roomNumber = str(roomNumber)
        deploycode = str(deploycode)
        orgchartmanager = str(orgchartmanager)
        utilityaccount = str(utilityaccount)

        attrs = {}
        attrs['objectClass'] = [
            'top', 'posixAccount',
            'person', 'organizationalPerson',
            'inetOrgPerson', 'yourdomain', 'extensibleobject']
        attrs['uid'] = username
        attrs['cn'] = full_name
        namesplit = full_name.split()
        if len(namesplit) == 2:
            attrs['givenName'] = namesplit[0]
            attrs['sn'] = namesplit[1]
        elif len(namesplit) == 1:
            attrs['givenName'] = namesplit[0]
            attrs['sn'] = ''
        else:
            attrs['givenName'] = ''
            attrs['sn'] = ''
        attrs['mail'] = email
        attrs['homeDirectory'] = '/home/%s' % username
        attrs['loginShell'] = shell
        attrs['gidNumber'] = '1008'
        attrs['uidNumber'] = str(int(self.last_uid) + 1)
        attrs['nsAccountLock'] = 'false'

        # YourDomain object
        attrs['title'] = title
        attrs['manager'] = manager
        attrs['departmentNumber'] = departmentNumber
        attrs['roomNumber'] = roomNumber
        attrs['deploycode'] = deploycode
        attrs['orgchartmanager'] = orgchartmanager
        attrs['utilityaccount'] = utilityaccount

        ldif = modlist.addModlist(attrs)
        self.connection.add_s('uid=%s' % username+','+_baseDN, ldif)

        c.new_account = True
        c.full_name = full_name
        c.username = username
        c.password = GeneratePassword(10)

        # Create the vpn-client for that user
        if utilityaccount == 'false':
            run_ssh_command('vpn_machine',
                './vpn-client.sh %s' % username)

        # Send Welcome Email
        self.update_attribute(
            'uid=%s' % username+','+_baseDN,
            'userPassword', c.password)
        if attrs['mail']:
            try:
                send_email(render('email/ldap_account.mako'),
                'Welcome to Yourdomain!', email_to=attrs['mail'])
            except Exception as e:
                print e

    def create_group(self, groupname, description):
        groupname = str(groupname)
        description = str(description)
        attrs = {}
        attrs['objectClass'] = [
                'groupOfUniqueNames', 'top' ]
        attrs['cn'] = groupname
        attrs['description'] = description
        attrs['uniqueMember'] = []
        ldif = modlist.addModlist(attrs)
        self.connection.add_s(
                'cn=%s,ou=Groups,dc=yourdomain,dc=com' % groupname, ldif)

    @property
    def last_uid(self):
        highest_uid = 0
        for user in self.search_users():
            if user[1].has_key('uidNumber'):
                if user[1]['uidNumber'][0] > highest_uid:
                    highest_uid = user[1]['uidNumber'][0]
        return highest_uid

    def findUser(self, username, use_name=False, Attrs=None):
        if use_name:
            try:
                user_data = self.search(
                    Filter='gecos=%s' % (username),
                    Attrs=Attrs)[0]
            except:
                return None
        else:
            try:
                user_data = self.search(
                    Filter='uid=%s' % (username),
                    Attrs=Attrs)[0]
            except:
                return None

        if not user_data[0]:
            return None
        return user_data

    def deleteUser(self, userDN):
        self.connection.delete(userDN)

    @staticmethod
    def _makepasswd(password):
        return "{SHA}" + base64.encodestring(sha1(password).digest())


