import pycontrol.pycontrol as pc

class LoadBalancer(object):
    def __init__(self, ip, username=None, password=None):
        self.hostname = ip
        if not username:
            self.username = 'apiuser'
        else: self.username = username

        if not password:
            self.password = 'apipass'
        else: self.password = password

        self.b = pc.BIGIP(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                fromurl=True,
                wsdls = ['LocalLB.PoolMember', 'LocalLB.Pool'])

    def get_pools(self):
        return self.b.LocalLB.Pool.get_list()

    def get_member_status(self, pool):
        if len(pool) > 1:
            return self.b.LocalLB.PoolMember\
                    .get_session_enabled_state(pool_names = pool)
        else:
            return self.b.LocalLB.PoolMember\
                    .get_session_enabled_state(pool_names = [pool])

    def create_pool(self, pool_name, members):
        memberlist = []
        try:
            lbmeth = self.b.LocalLB.Pool\
                    .typefactory.create('LocalLB.LBMethod')
            self.b.LocalLB.Pool.create(
                    pool_names = [pool_name], lb_methods= \
                    [lbmeth.LB_METHOD_ROUND_ROBIN], members = [members])
            return True
        except:
            return False

    def _member_factory(self, member):
        '''
        Produces a Common.IPPortDefinition object per member ip:port combination
        object per member ip:port combination. Add these to Common.IPPortDefinitionSequence.

        args: a pycontrol LocalLB.PoolMember object and an ip:port
        combination that you'd like to add.
        '''

        ip,port = member.split(':')
        pmem = self.b.LocalLB.PoolMember.typefactory.create('Common.IPPortDefinition')
        pmem.address = ip
        pmem.port = int(port)
        return pmem

    def _session_state_factory(self, members):
        '''
        Returns session state objects. Returns a list of session state objects with associated
        members.
        '''
        session_states = []

        # create a type of: 'LocalLB.PoolMember.MemberSessionState'
        # Inside of this type, you'll see that it expects a pool member as an
        # attribute. Let's create that, set our attributes (address, port), and add it to sstate
        # above.

        for x in members:
            sstate = self.b.LocalLB.PoolMember.typefactory.create('LocalLB.PoolMember.MemberSessionState')
            sstate.member = self._member_factory(x)
            sstate.session_state = 'STATE_DISABLED'
            session_states.append(sstate)
        return session_states

        '''
        # The session state sequence object. Takes a list of 'member session state'
        # objects.Wrap the members in a LocalLB.PoolMember.MemberSessionStateSequence
        sstate_seq = b.LocalLB.PoolMember.typefactory.create('LocalLB.PoolMember.MemberSessionStateSequence')

        # 'item' is an attribute that maps to a list of 'Common.IPPortDefinition' objects.
        sstate_seq.item = session_state_factory(b, members)
        '''

    def disable_members(self, pool, members):
        sstate_seq = self.b.LocalLB.PoolMember.typefactory.create(
                'LocalLB.PoolMember.MemberSessionStateSequence')
        sstate_seq.item = self._session_state_factory(members)
        for i,x in enumerate(sstate_seq.item):
            sstate_seq.item[i].session_state = 'STATE_DISABLED'
        try:
            self.b.LocalLB.PoolMember.set_session_enabled_state(
                    pool_names = [pool],
                    session_states = [sstate_seq])
        except Exception, e:
            print e

    def enable_members(self, pool, members):
        sstate_seq = self.b.LocalLB.PoolMember.typefactory.create(
                'LocalLB.PoolMember.MemberSessionStateSequence')
        sstate_seq.item = self._session_state_factory(members)
        for i,x in enumerate(sstate_seq.item):
            sstate_seq.item[i].session_state = 'STATE_ENABLED'
        try:
            self.b.LocalLB.PoolMember.set_session_enabled_state(\
                    pool_names = [pool],
                    session_states = [sstate_seq])
        except Exception, e:
            print e

    def remove_members(self, pool, members):
        try:
            self.b.LocalLB.Pool.remove_member([pool], [members])
        except Exception, e:
            print e

    def add_members(self, pool, members):
        try:
            self.b.LocalLB.Pool.add_member([pool], [members])
        except Exception, e:
            print e

    def delete_pool(self, pool):
        try:
            self.b.LocalLB.Pool.delete_pool(pool)
        except Exception, e:
            print e

