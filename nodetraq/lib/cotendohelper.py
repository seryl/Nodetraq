from cotendo import CotendoHelper
from couchdbhelper import CouchHelper
from difflib import unified_diff
from emailhelper import send_email

class NodetraqCotendo(CotendoHelper):
    def __init__(self):
        super(NodetraqCotendo, self).__init__(
                "apiuser", "apipassword")

    def GrabDNS(self, domain, environment,
                local=False, revision=None):
        """
        GrabDNS with a local option. If local is true,
        it reads from the local couchdb instance.

        The reivision represents the couchdb revision.
        """
        if local:
            couch = CouchHelper('http://localhost:5984', 'nodetraq')
            view = couch.get_view('dns', 'configs')
            for row in view:
                if row.value.has_key('config'):
                    self.ImportDNS(row.value['config'], row.value['token'])
                    break
        else:
            self.dns = self.dns_get_conf(domain, environment)

    def EmailDiffs(self, prod_config, staging_config,
                   email_from='admin@yourdomain',
                   email_to=['email_user@yourdomain']):
        prod_config = prod_config.splitlines(1)
        staging_config = staging_config.splitlines(1)
        diff = ''.join(unified_diff(prod_config, staging_config,
                            'production', 'staging'))
        diff = diff.replace('\n', '<br />')
        diff = diff.replace('  ', '&nbsp&nbsp')
        return send_email(
            'Cotendo Updates:<br />%s' % diff,
            'Cotendo DNS Update', email_from, email_to)

