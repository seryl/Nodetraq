from urllib import urlencode
from urlparse import urlparse
from webhelpers.html import literal

def generate_sort(url, current_sort, key):
    uri = urlparse(url)
    path = uri.path
    query = None
    if not current_sort or current_sort != 'asc':
        current_sort = 'asc'
    else:
        current_sort = 'desc'

    if uri.query:
        query = [tuple(q.split('=')) for q \
                     in uri.query.split('&')]
    if query:
        query = [(k,v) for k,v in query if k != 'sort']
        new_url = uri.path + '?sort=' + key + ':' + \
            current_sort
        if query:
            new_url += '&' + urlencode(query)
    else:
        new_url = uri.path + '?sort=' + \
            key + ':' + current_sort
    return literal(new_url)

