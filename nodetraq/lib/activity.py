from nodetraq.model.activity import Activity, ActivityType, Changeset
from nodetraq.model.meta import Session
from nodetraq.model.nodes import Node, Group, Studio, Game
#from nodetraq.model.inventory import Inventory
from pylons import url

class ActivityEngine(object):

    class NodeItem(object):
        def __init__(self, Session, user_id):
            self.Session = Session
            self.user_id = user_id

        def create(self, data):
            node = Node()
            changes = []
            for k,v in data.iteritems():
                setattr(node, k, v)
                cs = Changeset()
                cs.field = k
                cs.old_value = v
                self.Session.add(cs)
                changes.append(cs)

            self.Session.add(node)

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'node')\
                    .filter(ActivityType.action == 'add')\
                    .first().id
            activity.link = 'Node (Added): %s' % node.hostname
            activity.changesets = changes

            self.Session.add(activity)
            self.Session.commit()

            return {"status": "Added %s" % node.hostname,
                    "info": { "id": node.id } }

        def create_many(self, data_set):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'node')\
                    .filter(ActivityType.action == 'add')\
                    .first().id
            activity.children = []

            self.Session.add(activity)

            for data in data_set['items']:
                node = Node()
                sub_activity = Activity()
                sub_activity.activity_type_id = activity.activity_type_id
                sub_activity.user_id = self.user_id
                sub_activity.changesets = []

                for k,v in data.iteritems():
                    setattr(node, k, v)
                    cs = Changeset()
                    cs.field = k
                    cs.old_value = v
                    self.Session.add(cs)
                    sub_activity.changesets.append(cs)

                self.Session.add(sub_activity)
                self.Session.add(node)
                activity.children.append(sub_activity)

            activity.link = 'Nodes (Added): %s new nodes added' % len(
                   activity.children)
            self.Session.add(activity)
            self.Session.commit()

            return 'Added %s groups' % len(activity.children)

        def destroy(self, item_id):
            node = self.Session.query(Node)\
                    .filter(Node.id == item_id)\
                    .first()
            hostname = node.hostname

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'node')\
                    .filter(ActivityType.action == 'remove')\
                    .first().id
            activity.link = 'Node (Removed): %s' % hostname
            self.Session.add(activity)

            self.Session.delete(node)
            self.Session.commit()

            return 'Removed %s' % hostname

        def destroy_many(self, item_ids):
            changes = []
            for item_id in item_ids:
                node = self.Session.query(Node)\
                        .filter(Node.id == item_id)\
                        .first()
                if node:
                    cs = Changeset()
                    cs.old_value = node.hostname
                    self.Session.add(cs)

            if not changes:
                return False
            removed = len(changes)

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'node')\
                    .filter(ActivityType.action == 'remove')\
                    .first().id
            activity.link = 'Nodes (Removed): %s nodes' % removed
            activity.changesets = changes
            self.Session.add(activity)

            for n in changes:
                self.Session.delete(n)
            self.Session.commit()

            return 'Removed %s nodes' % removed

        def update(self, item_id, data):
            changes = []
            convert_vals = {
                    'rack': int,
                    'rack_u': int,
                    'cpu_count': int,
                    'cpu_speed': float,
                    'memory': float,
                    'xen_instance': int,
                    'nagios': int,
                    'puppet': int, }
            model_vals = {
                'game': Game
                }

            node = self.Session.query(Node).filter(Node.id == item_id).first()
            old_name = node.hostname

            if 'game' not in data:
                data['game'] = None

            for k,v in data.iteritems():
                if k in ['primary_mac', 'secondary_mac']:
                    v = v.replace(':', '')
                if k in model_vals:
                    cs = Changeset()
                    cs.field = k
                    cs.old_value = getattr(node, k)
                    if type(cs.old_value) == 'game':
                        cs.old_value = cs.old_value.name
                    else:
                        cs.old_value = ''
                    if v:
                        setattr(node, k, Session.query(
                                model_vals[k]).filter(model_vals[k].id == int(v)).first())
                    else:
                        setattr(node, k, None)
                    cs.new_value = getattr(node, k)
                    if type(cs.new_value) == 'game':
                        cs.new_value = cs.new_value.name
                    else:
                        cs.new_value = ''
                    self.Session.add(cs)
                    changes.append(cs)
                    continue
                elif k in convert_vals:
                    if v == '':
                        v = None
                        if getattr(node, k) == v:
                            continue
                    else:
                        v = convert_vals[k](v)
                elif v == '':
                    v = None
                if getattr(node, k) != v:
                    cs = Changeset()
                    cs.field = k
                    cs.old_value = getattr(node, k)
                    cs.new_value = v
                    self.Session.add(cs)
                    changes.append(cs)

                    setattr(node, k, v)

            if not changes:
                return 'No changes were made'

            self.Session.add(node)

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'node')\
                    .filter(ActivityType.action == 'update')\
                    .first().id

            change_count = len(changes)
            has_hostname = False
            ip_change = False
            rack_change = False
            rack_info = {}
            for change in changes:
                if change.field == 'hostname':
                    activity.link = 'Node (Update): %s ->  %s' % (
                            change.old_value, change.new_value)
                    has_hostname = True
                    new_hostname = change.new_value

                if change.field in ['primary_ip']:
                    ip_change = True
                    ip_info = {'old': change.old_value, 'new': change.new_value}

                if change.field in ['rack', 'rack_u']:
                    rack_change = True
                    rack_info[change.field] = {
                        'old': change.old_value,
                        'new': change.new_value}

            if has_hostname:
                hname = new_hostname
            else:
                hname = old_name

            if not activity.link:
                activity.link = 'Node (Update): %s' % old_name

            activity.changesets = changes

            self.Session.add(activity)
            self.Session.commit()

            if has_hostname:
                return 'Updated %s -> %s' % (old_name, new_hostname)
            else:
                return 'Updated %s' % old_name

        '''
        def update_many(self, item_ids, data):
            changes = []
            convert_vals = {
                'rack': int,
                'rack_u': int,
                'cpu_count': int,
                'cpu_speed': float,
                'memory': float,
                'xen_instance': int,
                'nagios': int,
                'puppet': int,}

            activity = Activity()
            activity.user_id = self.user_id
            activity.children = []
            is_nagios = False

            if data.has_key('enable_nagios'):
                is_nagios = True
                activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'nagios')\
                    .filter(ActivityType.action == 'enable')\
                    .first().id
            elif data.has_key('disable_nagios'):
                is_nagios = True
                activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'nagios')\
                    .filter(ActivityType.action == 'disable')\
                    .first().id
            else:
                activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'node')\
                    .filter(ActivityType.action == 'update')\
                    .first().id
                activity.link = 'Node: %s updated nodes' % changes

            self.Session.add(activity)

            if is_nagios:
                for node in self.Session.query(Node)\
                        .filter(Node.id.in_(item_ids))\
                        .all():
                    node

            # activity.changesets = changes

            # for node in self.Session.query(Node)\
            #    .filter(Node.id.in_(item_ids))\
            #    .all():


            self.Session.add(activity)
            self.Session.commit()

            return 'Updated %s nodes' % changes
            pass
        '''

        def import_data(self, data):
            pass

        def export_data(self, data):
            pass

    class GroupItem(object):
        def __init__(self, Session, user_id):
            self.Session = Session
            self.user_id = user_id

        def create(self, data):
            group = Group()
            for k,v in data.iteritems():
                if k == 'name':
                    v = v.replace(' ', '-')
                setattr(group, k, v)
            self.Session.add(group)
            # self.Session.commit()

            cs = None
            if group.description:
                cs = Changeset()
                cs.field = 'description'
                cs.old_value = group.description
                self.Session.add(cs)
                # self.Session.commit()

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'group')\
                    .filter(ActivityType.action == 'add')\
                    .first().id
            activity.link = 'Group (Added): %s' % group.name
            if cs:
                activity.changesets = [cs]
            self.Session.add(activity)
            self.Session.commit()

            return 'Added %s' % group.name

        def create_many(self, data_set):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'group')\
                    .filter(ActivityType.action == 'add')\
                    .first().id
            activity.children = []

            self.Session.add(activity)

            for data in data_set['items']:
                group = Group()
                sub_activity = Activity()
                sub_activity.activity_type_id = activity.activity_type_id
                sub_activity.user_id = self.user_id
                sub_activity.changesets = []

                for k,v in data.iteritems():
                    setattr(group, k, v)
                    cs = Changeset()
                    cs.field = k
                    cs.old_value = v
                    self.Session.add(cs)
                    sub_activity.changesets.append(cs)

                self.Session.add(sub_activity)
                self.Session.add(group)
                activity.children.append(sub_activity)

            activity.link = 'Groups (Added): %s new groups' % len(
                    activity.children)
            self.Session.add(activity)
            self.Session.commit()

            return 'Added %s groups' % len(activity.children)

        def destroy(self, item_id):
            group = self.Session.query(Group)\
                    .filter(Group.id == item_id)\
                    .first()
            group_name = group.name

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'group')\
                    .filter(ActivityType.action == 'remove')\
                    .first().id
            activity.link = 'Group (Removed): %s' % group_name
            self.Session.add(activity)
            self.Session.commit()

            self.Session.delete(group)
            self.Session.commit()

            return 'Removed %s' % group_name

        def destroy_many(self, item_ids):
            changes = []
            for item_id in item_ids:
                group = self.Session.query(Group)\
                        .filter(Group.id == item_id)\
                        .first()
                if group:
                    cs = Changeset()
                    cs.old_value = group.name
                    self.Session.add(cs)
                    self.Session.commit()
                    changes.append(cs)

            if not changes:
                return False
            removed = len(changes)

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'group')\
                    .filter(ActivityType.action == 'remove')\
                    .first().id
            activity.link = 'Group (Removed): %s groups' % removed
            activity.changesets = changes
            self.Session.add(activity)
            self.Session.commit()

            for g in changes:
                self.Session.delete(g)
            self.Session.commit()

            return 'Removed %s groups' % removed

        def update(self, item_id, data):
            group = self.Session.query(Group)\
                    .filter(Group.id == item_id)\
                    .first()

            if not group:
                return False
            old_name = group.name

            changes = []
            for k,v in data.iteritems():
                if k == 'name':
                    v = v.replace(' ', '-')
                if not getattr(group, k) == v:
                    cs = Changeset()
                    cs.field = k
                    cs.old_value = getattr(group, k)
                    cs.new_value = v
                    self.Session.add(cs)
                    changes.append(cs)

                    setattr(group, k, v)

            if not changes:
                return False

            self.Session.add(group)

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'group')\
                    .filter(ActivityType.action == 'update')\
                    .first().id

            for change in changes:
                if change.field == 'name':
                    activity.link = 'Group (Update): %s -> %s' % (
                            change.old_value, change.new_value)

            if not activity.link:
                activity.link = 'Group (Update): %s' % old_name

            activity.changesets = changes

            self.Session.add(activity)
            self.Session.commit()

            return 'Updated %s' % old_name

        def update_many(self, item_ids, data):
            '''Given node ids and the group names to remove them from'''
            activity = Activity()
            activity.user_id = self.user_id
            activity.children = []

            if data.has_key('add_groups'):
                activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'group')\
                    .filter(ActivityType.action == 'add')\
                    .first().id
            elif data.has_key('remove_groups'):
                activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'group')\
                    .filter(ActivityType.action == 'remove')\
                    .first().id
            elif data.has_key('add_nagios'):
                activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'nagios')\
                    .filter(ActivityType.action == 'enable')\
                    .first().id
            elif data.has_key('remove_nagios'):
                activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'nagios')\
                    .filter(ActivityType.action == 'disable')\
                    .first().id
            elif data.has_key('add_puppet'):
                activity.activity_type_id = self.Session.query(ActivityType)\
                    .filter(ActivityType.name == 'puppet')\
                    .filter(ActivityType.action == 'enable')\
                    .first().id
            elif data.has_key('remove_puppet'):
                activity.activity_type_id = self.Session.query(ActivityType)\
                    .filter(ActivityType.name == 'puppet')\
                    .filter(ActivityType.action == 'disable')\
                    .first().id
            else:
                return False

            if data.has_key('add_nagios') or data.has_key('remove_nagios'):
                if data.has_key('add_nagios'):
                    nagios_status = True
                else:
                    nagios_status = False

                changes = 0
                for cur_node in self.Session.query(Node)\
                        .filter(Node.id.in_(item_ids))\
                        .all():
                    if not cur_node.nagios == nagios_status:
                        changes += 1
                        cs = Changeset()
                        cs.field = 'nagios'
                        cs.old_value = str(cur_node.nagios)
                        cs.new_value = str(nagios_status)

                        cur_node.nagios = nagios_status
                        self.Session.add(cur_node)

                        sub_activity = Activity()
                        sub_activity.user_id = activity.user_id
                        sub_activity.activity_type_id = activity.activity_type_id
                        sub_activity.link = cur_node.hostname
                        sub_activity.changesets = [cs]
                        self.Session.add(sub_activity)
                        activity.children.append(sub_activity)
                        self.Session.add(activity)
                        self.Session.commit()

            elif data.has_key('add_puppet') or data.has_key('remove_puppet'):
                if data.has_key('add_puppet'):
                    puppet_status = True
                else:
                    puppet_status = False

                changes = 0
                for cur_node in self.Session.query(Node)\
                        .filter(Node.id.in_(item_ids))\
                        .all():
                    if not cur_node.puppet == puppet_status:
                        changes += 1
                        cs = Changeset()
                        cs.field = 'puppet'
                        cs.old_value = str(cur_node.puppet)
                        cs.new_value = str(puppet_status)

                        cur_node.puppet = puppet_status
                        self.Session.add(cur_node)

                        sub_activity = Activity()
                        sub_activity.user_id = activity.user_id
                        sub_activity.activity_type_id = activity.activity_type_id
                        sub_activity.link = cur_node.hostname
                        sub_activity.changesets = [cs]
                        self.Session.add(sub_activity)
                        activity.children.append(sub_activity)
                        self.Session.add(activity)
                        self.Session.commit()
            else:
                self.Session.add(activity)
                groups = self.Session.query(Group)\
                    .filter(Group.name.in_(data['groups']))\
                    .all()
                if not groups:
                    return False

                changes = 0
                for node in self.Session.query(Node)\
                        .filter(Node.id.in_(item_ids))\
                        .all():

                    old_groups = node.groups
                    if data.has_key('add_groups'):
                        node.groups = node.groups + \
                            [g for g in groups if g not in node.groups]
                    elif data.has_key('remove_groups'):
                        node.groups = [\
                            g for g in node.groups if g not in groups]

                    test = list(set(node.groups).difference(set(old_groups)))
                    if data.has_key('remove_groups'):
                        test = not test
                    if test:
                        self.Session.add(node)
                        self.Session.commit()

                        cs = Changeset()
                        cs.field = 'groups'
                        cs.old_value = ', '.join(['%s' % g for g in old_groups])
                        cs.new_value = ', '.join(['%s' % g for g in node.groups])
                        self.Session.add(cs)
                        self.Session.commit()

                        sub_activity = Activity()
                        sub_activity.user_id = activity.user_id
                        sub_activity.activity_type_id = activity.activity_type_id
                        sub_activity.link = node.hostname
                        sub_activity.changesets = [cs]
                        self.Session.add(sub_activity)
                        activity.children.append(sub_activity)
                        self.Session.add(activity)
                        self.Session.commit()
                        changes += 1

                if changes == 0:
                    return 'No changes were made'

                if data.has_key('add_groups'):
                    activity.link = 'Group (Update): Added %s nodes to %s' % (changes, ', '.join(data['groups']))
                else:
                    activity.link = 'Group (Update): Removed %s nodes from %s' % (changes, ', '.join(data['groups']))

                self.Session.add(activity)
                self.Session.commit()

                return activity.link[16:]

        def import_data(self, data):
            pass

        def export_data(self, data):
            pass

    class LbItem(object):
        def __init__(self, Session, user_id):
            self.Session = Session
            self.user_id = user_id

        def create(self, data):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                .query(ActivityType)\
                .filter(ActivityType.name == 'loadbalancer')\
                .filter(ActivityType.action == 'add')\
                .first().id

            activity.link = 'Added pool %s' % data['pool']
            self.Session.add(activity)
            self.Session.commit()

            return 'Pool %s created' % data['pool']

        def update(self, item_id, data):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                .query(ActivityType)\
                .filter(ActivityType.name == 'loadbalancer')\
                .filter(ActivityType.action == 'update')\
                .first().id

            if data['type'] == 'enable':
                # Enable hosts on a lb pool
                activity.link = 'Enabled %s in pool %s' % (
                    ', '.join(data['hosts']), data['pool'])
            elif data['type'] == 'disable':
                # Disable hosts on a lb pool
                activity.link = 'Disabled %s in pool %s' % (
                    ', '.join(data['hosts']), data['pool'])
            elif data['type'] == 'add':
                # Add hosts to a lb pool
                activity.link = 'Added %s to pool %s' % (
                    ', '.join(data['hosts']), data['pool'])
            elif data['type'] == 'remove':
                # Remove host from lb pool
                activity.link = 'Removed %s from pool %s' % (
                    ', '.join(data['hosts']), data['pool'])

            activity.description = ''
            self.Session.add(activity)
            self.Session.commit()

            return activity.link

        def update_many(self, item_id, data):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                .query(ActivityType)\
                .filter(ActivityType.name == 'loadbalancer')\
                .filter(ActivityType.action == 'update')\
                .first().id

            self.Session.add(activity)
            self.Session.commit()

            if data['type'] == 'enable':
                # Enable hosts on a lb pool
                activity.link = 'Enabled %s in pool %s' % (
                    ', '.join(data['hosts']), data['pool'])
            elif data['type'] == 'disable':
                # Disable hosts on a lb pool
                activity.link = 'Disabled %s in pool %s' % (
                    ', '.join(data['hosts']), data['pool'])
            elif data['type'] == 'add':
                # Add hosts to a lb pool
                activity.link = 'Added %s to pool %s' % (
                    ', '.join(data['hosts']), data['pool'])
            elif data['type'] == 'remove':
                # Remove host from lb pool
                activity.link = 'Removed %s from pool %s' % (
                    ', '.join(data['hosts']), data['pool'])

            for host in data['hosts']:
                sub_act = Activity()
                sub_act.user_id = self.user_id
                sub_act.activity_type_id = activity\
                    .activity_type_id
                if data['type'] == 'enable':
                    sub_act.description = 'Enabled %s from pool %s' % (
                        host, data['pool'])
                elif data['type'] == 'disable':
                    sub_act.description = 'Disabled %s from pool %s' % (
                        host, data['pool'])
                elif data['type'] == 'add':
                    sub_act.description = 'Added %s from pool %s' % (
                        host, data['pool'])
                elif data['type'] == 'remove':
                    sub_act.description = 'Removed %s from pool %s' % (
                        host, data['pool'])
                self.Session.add(sub_act)
                activity.children.append(sub_act)

            self.Session.add(activity)
            self.Session.commit()

        def destroy(self, data):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                .query(ActivityType)\
                .filter(ActivityType.name == 'loadbalancer')\
                .filter(ActivityType.action == 'remove')\
                .first().id
            activity.link = 'Removed pool %s' % data['pools'][0]
            self.Session.add(activity)
            self.Session.commit()

            return 'Removed pool %s' % data['pools'][0]

        def destroy_many(self, data):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                .query(ActivityType)\
                .filter(ActivityType.name == 'loadbalancer')\
                .filter(ActivityType.action == 'remove')\
                .first().id

    class InventoryItem(object):
        def __init__(self, Session, user_id):
            self.Session = Session
            self.user_id = user_id

        def create(self, data):
            inventory = Inventory()
            for k,v in data.iteritems():
                setattr(inventory, k, v)
            self.Session.add(inventory)
            self.Session.commit()

            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                    .query(ActivityType)\
                    .filter(ActivityType.name == 'inventory')\
                    .filter(ActivityType.action == 'add')\
                    .first().id
            #activity.link = 'Inventory: %s added' %

            activity.description = '%s' % node
            self.Session.add(activity)
            self.Session.commit()

            return activity.link

        def create_many(self, data_set):
            pass

        def destroy(self, item_id):
            pass

        def destroy_many(self, data_set):
            pass

        def update(self, item_id, data):
            pass

        def import_data(self, data):
            pass

        def export_data(self, data):
            pass

    class UserItem(object):
        def __init__(self, Session, user_id):
            self.Session = Session
            self.user_id = user_id

        def create(self, data):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                .query(ActivityType)\
                .filter(ActivityType.name == 'user')\
                .filter(ActivityType.action == 'create')\
                .first().id

            activity.link = 'Created new user: %s (%s)' % (
                data['name'], data['username'])

            self.Session.add(activity)
            self.Session.commit()

            return activity.link

        def create_many(self, data_set):
            pass

        def destroy(self, item_id):
            pass

        def destroy_many(self, data_set):
            pass

        def update(self, item_id, data):
            activity = Activity()
            activity.user_id = self.user_id
            activity.activity_type_id = self.Session\
                .query(ActivityType)\
                .filter(ActivityType.name == 'user')\
                .filter(ActivityType.action == 'update')\
                .first().id

            activity.link = 'Updated user: %s' % data['account']
            desc = ''
            for k,v in data.iteritems():
                if k == 'account':
                    continue
                desc += " - > ".join([k, v])
                desc += "\n"
            activity.description = desc

            self.Session.add(activity)
            self.Session.commit()

            return activity.link

        def import_data(self, data):
            pass

        def export_data(self, data):
            pass


    _select_map = (
            ('node', NodeItem),
            ('group', GroupItem),
            ('inventory', InventoryItem),
            ('loadbalancer', LbItem),
            ('user', UserItem),
            )

    def __init__(self, Session, user_id):
        self.Session = Session
        self.user_id = user_id
        self.engine = None

    def _get_engine(self, item_type):
        self.engine = None
        for mapping in self._select_map:
            if item_type in mapping:
                self.engine = mapping[1](self.Session, self.user_id)

        if not self.engine:
            return (False, 'Invalid item type')

    def create(self, item_type, data):
        self._get_engine(item_type)
        return self.engine.create(data)

    def create_many(self, item_type, data_set):
        self._get_engine(item_type)
        return self.engine.create_many(data_set)

    def destroy(self, item_type, item_id):
        self._get_engine(item_type)
        return self.engine.destroy(item_id)

    def destroy_many(self, item_type, item_ids):
        self._get_engine(item_type)
        return self.engine.destroy_many(item_ids)

    def update(self, item_type, item_id, data):
        self._get_engine(item_type)
        return self.engine.update(item_id, data)

    def update_many(self, item_type, item_ids, data):
        self._get_engine(item_type)
        return self.engine.update_many(item_ids, data)

    def import_data(self, item_type, data):
        ''' Import a csv file for a given item type.
        '''
        self._get_engine(item_type)
        return self.engine.import_data(data)

    def export_data(self, item_type, data):
        '''Return a csv file for the requested dataset.

            {'item_ids': all} returns all data
            {'item_ids': [1, 15, ...]} returns specific data ids.
        '''
        self._get_engine(item_type)
        return self.engine.export_data(data)





