import logging
import couchdb
import json
import difflib

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render, user_level
from nodetraq.lib.cotendohelper import NodetraqCotendo

from couchdbhelper import CouchHelper

log = logging.getLogger(__name__)

ch = CouchHelper("http://localhost:5984")
ch.select("nodetraq")

class DnsController(BaseController):
    @user_level(0)
    def __before__(self):
        super(DnsController, self).__before__()

    #def index(self):
    #    return render('/dns/select_domain.mako')
    #    pass

    def index(self, domain='yourdomainhere'):
        c.title = "Nodetraq -- DNS"
        c.selected_page = "dns"
        c.subpage = "list"
        c.domain = domain

        cotendo = NodetraqCotendo()
        cotendo.GrabDNS(domain, 1)
        ch.select("nodetraq")

        # Sync views
        ch.sync_view('nodetraq/model/views')

        # Update CouchDB to have a copy of the latest dns entries.
        results = ch.get_view('dns', 'configs')
        doc = None
        for r in results.rows:
            if r.value['environment'] == 'staging':
                doc = couchdb.Document(r.value)
                cotendo.ImportDNS(r.value["config"], r.value['token'])
            if doc:
                if doc["config"] != cotendo.dns.config:
                    doc["config"] = cotendo.dns.config
                    doc["token"] = cotendo.dns.token
                    ch.save(doc)
        if not doc:
            doc = couchdb.Document({"doc_type": "dns",
                     "domain": domain,
                     "environment": "staging",
                     "token": cotendo.dns.token,
                     "config": cotendo.dns.config })
            ch.save(doc)

        c.records = cotendo.dns._entries
        return render('dns/list.mako')

    def save_edit(self, domain='yourdomainhere'):
        cotendo = NodetraqCotendo()
        cotendo.GrabDNS(domain, 1)

        # Update CouchDB to have a copy of the latest dns entries.
        results = ch.get_view('dns', 'configs')
        doc = None
        for r in results.rows:
            if r.value['environment'] == 'staging':
                doc = couchdb.Document(r.value)
                break

        if doc:
            if doc["config"] != cotendo.dns.config:
                doc["config"] = cotendo.dns.config
                ch.save(doc)
        else:
            doc = couchdb.Document({"doc_type": "dns",
                     "domain": domain,
                     "environment": "staging",
                     "token": cotendo.dns.token,
                     "config": cotendo.dns.config })
            ch.save(doc)

        return redirect(url(controller="dns", action="diff"))

    def add_record(self, domain='yourdomainhere'):
        c.title = "Nodetraq -- DNS - Add Record"
        c.selected_page = "dns"
        c.subpage = "add_record"
        c.domain = domain

        return render('dns/add_record.mako')

    def edit_record(self, domain='yourdomainhere', type=None, host=''):
        c.title = "Nodetraq -- DNS - Edit Record"
        c.selected_page = "dns"
        c.subpage = "edit_record"
        c.domain = domain

        cotendo = NodetraqCotendo()
        cotendo.GrabDNS(domain, 1)
        # check if record exists, if it does, update it otherwise
        results = ch.get_view('dns', 'configs')
        doc = None
        for r in results.rows:
            if r.value['environment'] == 'staging':
                cotendo.ImportDNS(r.value["config"], r.value['token'])
                doc = couchdb.Document(r.value)
                break

        c.record = cotendo.dns.get_record(type, host)
        if not c.record:
            session['flash'] = "Not a valid record"
            session.save()
            return redirect(url(controller="dns",
                                action="index", domain=domain))

        return render('/dns/edit_record.mako')

    def update_record(self, domain='yourdomainhere'):
        cotendo = NodetraqCotendo()
        cotendo.GrabDNS(domain, 1)

        # check if record exists, if it does, update it otherwise
        results = ch.get_view('dns', 'configs')
        doc = None
        for r in results.rows:
            if r.value['environment'] == 'staging':
                cotendo.ImportDNS(r.value["config"], r.value['token'])
                doc = couchdb.Document(r.value)
                break

        # Create record
        for item in request.params.iteritems():
            params = json.loads(item[0])
            break

        if 'host' not in params:
            params['host'] = ''
        record = cotendo.dns.CreateRecord(
            params['type'], params['host'], params['results'])

        cotendo.dns.add_record(record)

        if doc:
            if doc["config"] != cotendo.dns.config:
                doc["config"] = cotendo.dns.config
                doc["token"] = cotendo.dns.token
                ch.save(doc)
        else:
            doc = couchdb.Document({"doc_type": "dns",
                     "domain": domain,
                     "environment": "staging",
                     "token": cotendo.dns.token,
                     "config": cotendo.dns.config })
            ch.save(doc)

    def remove_record(self):
        for item in request.params.iteritems():
            params = json.loads(item[0])
            break
        domain = params['domain']
        cotendo = NodetraqCotendo()
        cotendo.GrabDNS(domain, 1)

        # check if record exists, if it does, update it otherwise
        results = ch.get_view('dns', 'configs')
        doc = None
        for r in results.rows:
            if r.value['environment'] == 'staging':
                cotendo.ImportDNS(r.value["config"], r.value['token'])
                doc = couchdb.Document(r.value)
                break

        cotendo.dns.del_record(params['type'], params['host'])

        if doc:
            if doc["config"] != cotendo.dns.config:
                doc["config"] = cotendo.dns.config
                doc["token"] = cotendo.dns.token
                ch.save(doc)
        else:
            doc = couchdb.Document({"doc_type": "dns",
                     "domain": domain,
                     "environment": "staging",
                     "token": cotendo.dns.token,
                     "config": cotendo.dns.config })
            ch.save(doc)

    def publish(self, domain='yourdomainhere'):
        c.title = "Nodetraq -- DNS - Publish"
        c.selected_page = "dns"
        c.subpage = "publish"
        c.domain = domain

        prod = NodetraqCotendo()
        prod.GrabDNS(domain, 1)
        staging = NodetraqCotendo()
        staging.GrabDNS(domain, 1)

        results = ch.get_view('dns', 'configs')
        for r in results.rows:
            if r.value['environment'] == 'staging':
                staging.ImportDNS(r.value["config"], r.value["token"])
                break

        staging_config = staging.dns.config.splitlines(1)
        prod_config = prod.dns.config.splitlines(1)

        diff = ''.join(difflib.unified_diff(
                prod_config, staging_config, 'production', 'staging'))

        c.diff = diff
        return render('/dns/publish.mako')

    def push(self, domain='yourdomainhere', rev=None):
        cotendo = NodetraqCotendo()
        cotendo.GrabDNS(domain, 1)

        prod_config = cotendo.dns.config
        results = ch.get_view('dns', 'configs')
        for r in results.rows:
            if r.value['environment'] == 'staging':
                staging_document = r.value
                break

        if rev:
            for d in ch.db.revisions(staging_document['_id']):
                if d['_rev'] == rev:
                    staging_document = d
                    break

        cotendo.ImportDNS(staging_document["config"], cotendo.dns.token)
        staging_config = cotendo.dns.config
        cotendo.UpdateDNS(domain, 1)
        cotendo.dns_publish_conf(domain)
        cotendo.EmailDiffs(prod_config, staging_config)

    def revert(self, domain='yourdomainhere'):
        c.title = "Nodetraq -- DNS - Publish"
        c.selected_page = "dns"
        c.subpage = "publish"
        c.domain = domain

        results = ch.get_view('dns', 'configs')
        for r in results.rows:
            if r.value['environment'] == 'staging':
                doc = couchdb.Document(r.value)
                break

        c.rev_list = []
        for d in ch.db.revisions(doc['_id']):
            c.rev_list.append((d['_rev'], d['_rev']))
        return render('/dns/revert.mako')

    def get_document_diff(self, domain='yourdomainhere', rev=None):
        cotendo = NodetraqCotendo()
        cotendo.GrabDNS(domain, 1)

        results = ch.get_view('dns', 'configs')
        for r in results.rows:
            if r.value['environment'] == 'staging':
                doc = couchdb.Document(r.value)
                break

        for d in ch.db.revisions(doc['_id']):
            if d['_rev'] == rev:
                doc = d

        if rev:
            c.diff = ''.join(difflib.unified_diff(
                    doc['config'].splitlines(1),
                    cotendo.dns.config.splitlines(1)))
        else:
            c.diff = ''.join(cotendo.dns.config.splitlines(1),
            difflib.unified_diff(doc['config'].splitlines(1)))

        return render('/diff/diff_table.mako')

    def pull_production(self, domain='yourdomainhere'):
        cotendo = NodetraqCotendo()
        cotendo.GrabDNS(domain, 1)

        results = ch.get_view('dns', 'configs')
        doc = None
        doc_list = ['production', 'staging']
        for r in results.rows:
            if r.value['environment'] in ['production', 'staging']:
                doc_list.remove(r.value['environment'])
                doc = couchdb.Document(r.value)
            if doc:
                if doc["config"] != cotendo.dns.config:
                    doc["config"] = cotendo.dns.config
                    doc["token"] = cotendo.dns.token
                    ch.save(doc)

        for d in doc_list:
            doc = couchdb.Document({"doc_type": "dns",
                     "domain": domain,
                     "environment": d,
                     "token": cotendo.dns.token,
                     "config": cotendo.dns.config })
            ch.save(doc)

    def get_new_record(self):
        json_data = json.loads(
            request.params.keys()[0])
        c.record_type = json_data['record_type']
        c.count = json_data['count']
        if not c.count:
            c.count = 0
        return render('/dns/new_record.mako')
