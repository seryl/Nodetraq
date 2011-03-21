from users import ActiveDirectory, LdapDirectory
from random import choice
import string
import ldap

def generate_password(length):
    return ''.join([
            choice(string.letters+string.digits)\
                for i in xrange(0, length)])

class ComboDirectory(object):
    def __init__(self, username, password, domain):
        self.ad = ActiveDirectory(
                server='ldaps://yourdomain:636',
            username=username, password=password,
            domain=domain)
        #self.l = LdapDirectory(username, password)

    def search_ad_users(self, username=None, attributes=None):
        if username:
            pass
        else:
            return self.ad.search(
                Filter="(&(objectClass=user))",
                Attrs=attributes)

    def search_ldap_users(self, username=None, attributes=None):
        if username:
            pass
        else:
            return self.l.search(
                Filter="(&(objectClass=user))",
                Attrs=attributes)

    def search_group(self, group=None, attributes=None):
        if group:
            pass
        else:
            return self.ad.search(
                Filter="(&(objectClass=group))",
                Attrs=attributes)

    def update_attribute(self, dn, attr, values,
            mode=ldap.MOD_REPLACE):
        self.ad.update_attribute(dn, attr, values, mode)
        return True

    def add_junk_record(self):
        add_record = [
            ('objectClass', ['person', 'user']),
            ('countryCode', ['0']),
            ('uid', ['junkuid']),
            ('name', ['junkid']),
            ('cn', ['Junk User'] ),
            ('sn', ['Bacon'] ),
            ('objectCategory', ['CN=Person,CN=Schema,CN=Configuration,DC=yourdomain,DC=com']),
            ('distinguishedName', ['CN=Junk User,OU=Users,OU=\\+Objects,Dc=yourdomain,DC=com']),
            ('userPrincipalName', ['junkuser@yourdomain']),
            ]
        self.ad.connection.add_s('CN=Junk User,OU=Users,OU=\\+Objects,Dc=yourdomain,DC=com', add_record)


    def create(self):
        pass

    def sync(self):
        pass

