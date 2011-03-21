import csv
import os

from nodetraq.model.meta import Session, metadata
from nodetraq.model.nodes import Node

node_replacements = [
        ('Hostname', 'hostname'),
        ('Service Tag', 'service_tag'),
        ('RACK', 'rack'),
        ('RACK U', 'rack_u'),
        ('Description', 'description'),
        ('Firmware Updated?', 'firmware'),
        ('Primary IP', 'primary_ip'),
        ('Secondary IP', 'secondary_ip'),
        ('Primary MAC', 'primary_mac'),
        ('Secondary MAC', 'secondary_mac'),
        ('root pw', 'root_password'),
        ('DRAC', 'drac_ip'),
        ('Xen Instance', 'xen_instance'),
        ]

def node_csv_import(filename):
    sReader = csv.reader(open(filename),
        delimiter=',',
        quotechar='"')

    schema = None
    data = []

    for row in sReader:
        if not schema:
            schema = row
        else:
            data.append(row)

    return (schema, data)

def node_csv2json(node_csv):
    json_hash = { 'nodes' : [] }
    schema, data = node_csv
    for i, key in enumerate(schema):
        for word, replacement in node_replacements:
            if key == word:
                schema[i] = replacement
                break
            else:
                schema[i] = None

    for item in data:
        zipped = zip(schema, item)
        item_hash = {}
        for k,v in zipped:
            item_hash[k] = v
        json_hash['nodes'].append(item_hash)

    return json_hash

def node_insert_db(node_data):
    schema, data = node_data

    # Setup schema to match attributes
    for i, key in enumerate(schema):
        for word, replacement in node_replacements:
            if key == word:
                schema[i] = replacement
                break
            else:
                schema[i] = None

    for item in data:
        node = Node()

        zipped = zip(schema, item)
        for key, value in zipped:
            if key:
                node.__setattr__(key, value)

        Session.add(node)
        Session.commit()

