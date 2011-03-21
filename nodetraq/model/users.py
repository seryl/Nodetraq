import ldap

from sqlalchemy import Column, Table, String, Integer, \
        Float, Boolean, TIMESTAMP, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

from nodetraq.model.meta import Base

_ldap_server = 'ldaps://ns1.yourdomain.com'
_ldap_server2 = 'ldaps://ns2.yourdomain.com'

_baseDN = 'ou=people,dc=yourdomain,dc=com'
_ops_dn = 'cn=ops,ou=groups,dc=yourdomain,dc=com'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(50))

def check_user(username, password):
    username = 'uid='+username+','+_baseDN
    l = ldap.initialize(_ldap_server)
    try:
        l.simple_bind_s(username, password)
        return (True,)
    except ldap.LDAPError, e:
        return False, e

