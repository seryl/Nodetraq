from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/:action', controller='error')
    map.connect('/error/:action/:id', controller='error')

    # Auth
    map.connect('/', controller='dashboard', action='index')
    map.connect('/login', controller='auth', action='index')
    map.connect('/logout', controller='auth', action='logout')

    # Activity
    map.connect('/activity', controller='activity', action='index')
    map.connect('/activity.xml', controller='activity', action='index', format='xml')
    map.connect('/activity.json', controller='activity', action='index', format='json')
    map.connect('/activity.atom', controller='activity', action='atom')

    # Dashboard
    map.connect('/dashboard', controller='dashboard', action='index')
    map.connect('/dashboard.atom', controller='dashboard', action='atom')

    # DNS
    with map.submapper(
        path_prefix='/dns', controller='dns') as c:
        c.connect('', action='index')
        c.connect('/edit/:domain', action='edit')
        c.connect('/edit_record/:domain/:type/', action='edit_record')
        c.connect('/edit_record/:domain/:type/:host', action='edit_record')
        c.connect('/get_document_diff/:domain/:rev', action='get_document_diff')
        c.connect('/push/:domain/:rev', action='push')
        c.connect('/push/:domain', action='push')

    # Groups
    with map.submapper(
        path_prefix='/groups', controller='groups') as c:
        c.connect('', action='index')
        c.connect('/new', action='new')
        c.connect('/delete', action='delete')
        c.connect('/create', action='create')
        c.connect('/update', action='update')
        c.connect('/add', action='add')
        c.connect('/:id', action='show')
        c.connect('/:id.:format', action='show')

    # Database Backups
    map.connect('/dbbackups/delete/:backup_id', controller='dbbackups', action='delete')
    with map.submapper(
        path_prefix='/nodes/:id/dbbackups', controller='dbbackups') as c:
        c.connect('', action='index')
        c.connect('/new', action='new')
        c.connect('/:backup_id/edit', action='edit')
        c.connect('/:backup_id/update', action='update')
        c.connect('/:backup_id/enable', action='enable')
        c.connect('/:backup_id/disable', action='disable')
        c.connect('/:backup_id/destroy', action='destroy')

    # Puppet
    with map.submapper(controller='puppet') as c:
        c.connect('/status/:hostname', action='status')
        with map.submapper(path_prefix='/nodes/puppet') as m:
            m.connect('/enable', action='addpuppet')
            m.connect('/disable', action='removepuppet')

    # Vhosts
    with map.submapper(
        path_prefix='/nodes/:id/vhosts', controller='vhosts') as c:
        c.connect('', action='index')
        c.connect('/new', action='new')
        c.connect('/:vhostid/', action='show')
        c.connect('/:vhostid/edit', action='edit')

    # Nodes
    with map.submapper(
        path_prefix='/nodes', controller='nodes') as c:
        c.connect('/new', action='new')
        c.connect('/edit/:id', action='edit')
        c.connect('/create', action='create')
        c.connect('/sendbatchedit', action='sendbatchedit')
        c.connect('/show_dbbackups', action='show_dbbackups')
        c.connect('/edit_bulk_dbbackups', action='edit_bulk_dbbackups')
        c.connect('/namelist', action='namelist')
        c.connect('/namelist.:format', action='namelist')
        c.connect('/importcsv', action='importcsv')
        c.connect('/upload_csv', action='upload_csv')
        c.connect('/updatemany', action='updatemany')
        c.connect('/addgroups', action='addgroups')
        c.connect('/removegroups', action='removegroups')
        c.connect('/edit_flags', action='edit_flags')
        c.connect('/clear_flags', action='clear_flags')
        c.connect('/update_flags', action='update_flags')
        c.connect('/batchedit', action='batchedit')
        c.connect('/create_comment', action='create_comment')
        c.connect('.:format', action='index')
        c.connect('', action='index')
        c.connect('/:id.:format', action='show')
        c.connect('/:id', action='show')
        c.connect('/updatebyname/:name.:format', action='updatebyname')
        c.connect('/namelist.:format', action='namelist')

        with map.submapper(
            path_prefix='/:id/comments/:commentid') as m:
            m.connect('/edit', action='edit_comment')
            m.connect('/destroy', action='destroy_comment')
            m.connect('/update', action='update_comment')

        c.connect('/nagios/enable', action='addnagios')
        c.connect('/nagios/disable', action='removenagios')
        c.connect('/update_disks/:hostname', action='update_disks')

        with map.submapper(
            path_prefix='/flags') as m:
            m.connect('/edit', action='edit_flags')
            m.connect('/clear', action='clear_flags')
            m.connect('/update', action='update_flags')

    # Studios
    with map.submapper(
        path_prefix="/studios", controller='nodes') as c:
        c.connect('', action='list_studios')
        c.connect('/create', action='create_studio')
        c.connect('/show/{id}', action='show_studio')
        c.connect('/edit/:id', action='edit_studio')
        c.connect('/update/:id', action='update_studio')
        c.connect('/destroy/:id', action='destroy_studio')
        c.connect('/new', action='new_studio')
        c.connect('/batch_update_studios', action='batch_update_studios')

    # Games
    with map.submapper(
        path_prefix="/games", controller='nodes') as c:
        c.connect('', action='list_games')
        c.connect('/create', action='create_game')
        c.connect('/show/{id}', action='show_game')
        c.connect('/edit/:id', action='edit_game')
        c.connect('/update/:id', action='update_game')
        c.connect('/destroy/:id', action='destroy_game')
        c.connect('/new', action='new_game')
        c.connect('/batch_update_games', action='batch_update_games')

    # Graphs
    map.connect('/graphs', controller='graphs', action='index')

    # Network
    map.connect('/network', controller='network', action='index')

    # Users
    with map.submapper(
        path_prefix='/users', controller='users') as c:
        c.connect('', action='search')
        c.connect('/list', action='index')
        c.connect('/edit/:account', action='edit')
        c.connect('/list/groups', action='list', type='groups')
        c.connect('/change_password/:account', action='change_password')
        c.connect('/reset_password/:account', action='reset_password')
        c.connect('/rename_user/:account', action='rename_user')
        c.connect('/rename_user_service/:account', action='rename_user_service')
        c.connect('/disable_user/:account', action='disable_user')
        c.connect('/enable_user/:account', action='enable_user')
        c.connect('/delete_user/:account', action='delete_user')
        c.connect('/update/:account', action='update')
        c.connect('/updategroup/:group', action='updategroup')
        c.connect('/editgroup/:group', action='editgroup')
        c.connect('/:group/members', action='group_members')
        c.connect('/:group/remove_members', action='remove_members')

    # Nagios
    with map.submapper(
        path_prefix='/nagios', controller='nagios') as c:
        c.connect('/acknowledge_svc_problem/:hostname',
                  action='acknowledge_svc_problem')
        c.connect('/acknowledge_host_problem/:hostname',
                  action='acknowledge_host_problem')
        c.connect('/remove_from_downtime/:service_type',
                  action='remove_from_downtime')

    # Loadbalancer
    with map.submapper(
        path_prefix='/loadbalancer', controller='loadbalancer') as c:
        c.connect('', action='index')
        c.connect('/show/:pool', action='show')
        c.connect('/disablehost.:format', action='disablehost')
        c.connect('/enablehost.:format', action='enablehost')
        c.connect('/addhost.:format', action='addhost')
        c.connect('/removehost.:format', action='removehost')
        c.connect('/:pool/comments/new', action='newcomment')
        c.connect('/:pool/comments/create', action='createcomment')

    # Pools
    map.connect('/pools', controller='pools', action='index')

    # Extras
    map.connect('/help', controller='help', action='index')
    map.connect('/hosts', controller='hosts', action='index')
    map.connect('/news', controller='news', action='index')
    map.connect('/tools', controller='tools', action='index')
    map.connect('/search', controller='search', action='index')
    map.connect('/wiki', controller='wiki', action='index')

    map.connect('/:controller/:action')
    map.connect('/:controller/:action/:id')

    return map
