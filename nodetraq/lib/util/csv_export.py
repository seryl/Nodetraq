from os import linesep

from nodetraq.model.meta import Session, metadata
from nodetraq.model.nodes import Node

def export_node(json_list):
    #for node in json_list:

    for id in id_list:
        node_list.append(
                Session.query(Node)
                .filter(Node.id == id).first())

    if node_list:
        keys = [v for v in dir(node_list[0]) if not v.startswith('_')]
        keys = [v for v in keys if not v in ignore_list]
    else:
        return

    csv = []
    csv.append(','.join(keys))

    for node in node_list:
        items = []
        for key in keys:
            attribute = node.__getattribute__(key)
            if attribute == None:
                items.append('')
            else:
                items.append(attribute)

        csv.append(','.join(items))

    return csv

