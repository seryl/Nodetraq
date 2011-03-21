import ldap

from nodetraq.model.users import User, _ldap_server, _ldap_server2, \
    _baseDN, _ops_dn
from users import ActiveDirectory, LdapDirectory
from nodetraq.model.meta import Session

directoryCN = 'directory_manager_cn'
directoryPassword = 'directory_password'
directoryDomain = 'your_domain'

def check_user(username, password):
    usernameDN = 'uid='+username+','+_baseDN
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, False)
    l = ldap.initialize(_ldap_server)

    dh = DirectoryHelper(
        directoryCN, directoryPassword, directoryDomain)

    try:
        l.simple_bind_s(usernameDN, password)
        filter = 'uid=*'+username+'*'
        retrieve_attributes = ['mail']

        base_result = l.result(l.search(
                _baseDN, ldap.SCOPE_SUBTREE,
                filter, retrieve_attributes))

        mail = None
        if base_result[0]:
            if base_result[1]:
                if base_result[1][0][1].has_key('mail'):
                    mail = base_result[1][0][1]['mail'][0]

            # Check if the user exists
            user = Session.query(User).filter(
                User.name == username).first()
            if not user:
                user = User()
                user.name = username
                if mail:
                    user.email = mail
                else:
                    user.email = username + '@yourdomain'
                Session.add(user)
                Session.commit()
            elif user.email != mail:
                if mail:
                    user.email = mail
                    Session.add(user)
                    Session.commit()
                elif user.email != username + '@yourdomain':
                    user.email = username + '@yourdomain'
                    Session.add(user)
                    Session.commit()

            # Get user groups
            userDN = dh.findUser(username)
            userGroups = dh.getUserGroups(username)

            user_level = 100
            if 'eng' in userGroups:
                user_level = 30
            if 'itops2' in userGroups:
                user_level = 10
            if 'ops' in userGroups:
                user_level = 0

            return (username, user.id, user_level)
        else:
            return (False,)

    except ldap.LDAPError, e:
        print e
        return False, e

class DirectoryHelper(object):
    def __init__(self, username, password, domain):
        try:
            self.ldap = LdapDirectory(
                server=_ldap_server,
                username=username, password=password,
                domain=domain)
        except:
            self.ldap = LdapDirectory(
                server=_ldap_server2,
                username=username, password=password,
                domain=domain)

        self.ad_to_ldap_map = {
            'sAMAccountName': 'uid',
            'mail': 'mail',
            'cn': 'cn',
            'name': 'gecos',
            'givenName': 'givenName',
            'sn': 'sn',
            'loginShell': 'loginShell',
            'uidNumber': 'uidNumber',
            'gidNumber': 'gidNumber',
            'userAccountControl': 'nsAccountLock'
           }

        self.ldap_to_ad_map = {
            'uid': 'sAMAccountName',
            'mail': 'mail',
            'cn': 'cn',
            'gecos': 'name',
            'givenName': 'givenName',
            'sn': 'sn',
            'loginShell': 'loginShell',
            'uidNumber': 'uidNumber',
            'gidNumber': 'gidNumber',
            'nsAccountLock': 'userAccountControl'
        }

    def search(self, BaseDN='DC=yourdomain,DC=com',
               Scope=ldap.SCOPE_SUBTREE, Filter=\
                   '(|(objectClass=person)(objectClass=groupofuniquenames))',
               Attrs=None):
        return self.ldap.search(BaseDN, Scope, Filter, Attrs)

    def search_users(self, BaseDN='DC=yourdomain,DC=com',
                     Scope=ldap.SCOPE_SUBTREE, Attrs=None, username=None):
        Attrs=['*', 'nsAccountLock']
        user_info = {}
        if username:
            ldap_filter = '(&(objectClass=person)(uid=%s))' % username
            user_info['ldap'] = self.ldap.search_users(
                Filter=ldap_filter, Attrs=Attrs)

        else:
            user_info = self.ldap.search_users(Attrs=Attrs)
        return user_info

    def update_attribute(self, username, attr, values,
                         mode=ldap.MOD_REPLACE):
        userDN = self.findUser(username)[0].lower()
        self.ldap.update_attribute(
            userDN, attr, values, mode)
        return True

    def update_group_attribute(self, group, attr, values,
                               mode=ldap.MOD_REPLACE):
        groupDN = 'cn=%s,ou=groups,dc=yourdomain,dc=com' % group
        self.ldap.update_attribute(
            groupDN, attr, values, mode)
        return True

    def update_dn(self, dn, dn_update):
        self.ldap.update_dn(dn, dn_update)
        return True

    def change_password(self, username, password):
        userDN = self.findUser(username)[0].lower()
        if not userDN:
            return False
        return self.ldap.update_attribute(
                userDN, 'userPassword', password)

    def reset_password(self, username):
        return self.ldap.reset_password(username)

    def findUser(self, username, use_name=False, Attrs=None):
        try:
            ldap_info = self.ldap.findUser(username, use_name, Attrs=Attrs)
        except:
            ldap_info = None

        return ldap_info

    def getUserGroups(self, username):
        try:
            userDN = self.findUser(username)[0].lower()
            group_membership = []
            for group in self.ldap.search_groups(
                Attrs=['uniqueMember', 'CN']):
                if group:
                    try:
                        if self.hasDN(userDN, group[1]['uniqueMember']):
                            group_membership.append(
                                group[1]['CN'][0])
                    except:
                        pass
            return group_membership
        except:
            return []

    def add_group(self, username, group):
        userDN = self.findUser(username)[0].lower()
        groupinfo = self.ldap.search_groups(
                Filter="(&(objectClass=groupofuniquenames)(cn=%s))" % group,
                Attrs=['uniqueMember', 'CN'])[0]
        if groupinfo[1].has_key('uniqueMember'):
            members = list(set(groupinfo[1]['uniqueMember']).union(set([userDN])))
        else:
            members = [userDN]

        self.ldap.update_attribute(groupinfo[0], 'uniqueMember', members)

    def remove_group(self, username, group):
        userDN = self.findUser(username)[0].lower()
        groupinfo = self.ldap.search_groups(
                Filter="(&(objectClass=groupofuniquenames)(cn=%s))" % group,
                Attrs=['uniqueMember', 'CN'])[0]
        members = groupinfo[1]['uniqueMember']
        for m in members:
            if m.lower() == userDN:
                userDN = m
        members = list(set(groupinfo[1]['uniqueMember']) - set([userDN]))
        self.ldap.update_attribute(groupinfo[0], 'uniqueMember', members)

    def set_groups(self, username, groups):
        userDN = self.findUser(username)[0].lower()
        current_groups = self.getUserGroups(username)
        remove_groups = list(set(current_groups) - set(groups))
        add_groups = list(set(groups) - set(current_groups))

        for group in remove_groups:
            self.remove_group(username, group)

        for group in add_groups:
            self.add_group(username, group)

    def getAllGroups(self):
        try:
            groups = [ g[1]['CN'][0] for g in \
                           self.ldap.search_groups(Attrs=['CN'])
                       ]
            return groups
        except:
            return []

    def getAllGroupsDN(self):
        try:
            groups = [ g[1] for g in \
                    self.ldap.search_groups(Attrs=['uniqueMember', 'CN'])
                    ]
            return groups
        except:
            return []

    def sync(self):
        pass

    def disable_user(self, username):
        return self.ldap.disable_user(username)

    def enable_user(self, username):
        return self.ldap.enable_user(username)

    def rename_user(self, username, targetname):
        pass

    @staticmethod
    def matchDN(left, right):
        left = left.lower().split(',')
        left = [l.strip() for l in left]
        right = right.split(',')
        right = [r.lower().strip() for r in right]
        if right == left:
            return True
        return False

    def hasDN(self, needle, haystack):
        for hay in haystack:
            if self.matchDN(needle, hay):
                return True
        return False

