from nodetraq.model.nodes import Group, Node
from sqlalchemy import and_, not_, or_

def get_fields_and_query(Session, cls, params):
    return generate_search_query(Session, cls,
            get_search_fields(params))

def get_search_fields(params):
    search_fields = []
    fields = [v for k,v in params.items() if 'fields[]' in k]
    for field in fields:
        field_hash = {}
        field_hash['name'] = field
        field_hash['operator'] = params['operators['+field+']']
        field_hash['value'] = params['['+field+'][]']

        search_fields.append(field_hash)

    return search_fields

def generate_search_query(Session, cls, search_fields, group_search=False):
    if not search_fields:
        return Session.query(cls), search_fields

    query = Session.query(cls)
    for sf in search_fields:
        fields = sf['value'].split(' ')
        if sf['operator'] == '=':
            if sf['name'] == 'groups':
                query = get_groups_query(Session, cls, query, sf)
            else:
                try:
                    queryset = tuple([
                        getattr(cls, sf['name']) == v for v in fields])
                    query = query.filter(or_(*queryset))
                except:
                    queryset = tuple([
                        getattr(cls, 'name') == v for v in fields])
                    query = query.filter(or_(*queryset))
        elif sf['operator'] == '!':
            if sf['name'] == 'groups':
                query = get_groups_query(Session, cls, query, sf)
            else:
                try:
                    queryset = tuple([
                        getattr(cls, sf['name']) != v for v in fields])
                    query = query.filter(and_(*queryset))
                except:
                    queryset = tuple([
                        getattr(cls, 'name') != v for v in fields])
                    query = query.filter(and_(*queryset))
        elif sf['operator'] == '~':
            if sf['name'] == 'groups':
                query = get_groups_query(Session, cls, query, sf)
            else:
                try:
                    queryset = tuple([
                        getattr(cls, sf['name']).like('%'+v+'%') for v in fields])
                    query = query.filter(or_(*queryset))
                except:
                    queryset = tuple([
                        getattr(cls, 'name').like('%'+v+'%') for v in fields])
                    query = query.filter(or_(*queryset))
        elif sf['operator'] == '>':
            try:
                query = query.filter(
                    getattr(cls, sf['name']) > sf['value'])

            except:
                query = query.filter(
                    getattr(cls, 'name') > sf['value'])
        elif sf['operator'] == '<':
            try:
                query = query.filter(
                    getattr(cls, sf['name']) < sf['value'])
            except:
                query = query.filter(
                    getattr(cls, 'name') < sf['value'])

    if not query:
        query = Session.query(cls)

    return query, search_fields

def get_groups_query(Session, cls, query, sf):
    if sf['operator'] == '=':
        group = Session.query(Group)\
            .filter(Group.name == sf['value']).first()
        if group:
            query = query.filter(
                getattr(cls, 'groups').contains(group))

    elif sf['operator'] == '!':
        group = Session.query(Group)\
            .filter(Group.name == sf['value']).first()
        if group:
            query = query.filter(not_(
                    getattr(cls, 'groups').contains(group)))

    elif sf['operator'] == '~':
        group = Session.query(Group).filter(
            Group.name.like('%'+sf['value']+'%')).first()
        if group:
            query = query.filter(
                    getattr(cls, 'groups').contains(group))

    return query

