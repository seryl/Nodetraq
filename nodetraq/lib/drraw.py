from string import ascii_lowercase
from sshwrapper import run_ssh_command

rrd_types = [
    'boottime', 'bytes_in',
    'bytes_out','cpu_aidle',
    'cpu_idle', 'cpu_nice',
    'cpu_num', 'cpu_speed',
    'cpu_system', 'cpu_user',
    'cpu_wio', 'disk_free',
    'disk_total', 'load_fifteen',
    'load_five', 'load_one',
    'mem_buffers', 'mem_cached',
    'mem_free', 'mem_shared',
    'mem_total', 'multicpu_idle0',
    'multicpu_intr0', 'multicpu_nice0',
    'multicpu_sintr0', 'multicpu_system0',
    'multicpu_user0', 'multicpu_wio0',
    'part_max_used', 'pkts_in',
    'pkts_out', 'proc_run',
    'proc_total', 'swap_free',
    'swap_total', 'lvm_VolGroup01',
    'mysqld_Com_select', 'mysqld_Com_insert'
    ]

def baseN(num, b, numerals=ascii_lowercase):
    if num < 0:
        return ''
    elif num == 0:
        return numerals[0]
    else:
        return baseN((num // b)-1, b).lstrip("0")\
                + numerals[num % b]

def alphaenum(collection):
    '''Generates an alphabetically indexed series:
    (a, coll[0]), (b, coll[1]) ...
    '''
    i = 0
    it = iter(collection)
    while 1:
        yield(baseN(i, 26), it.next())
        i += 1

def generate_rrd_filename(hostname, data_type):
    return '_'.join([hostname, data_type]) + '.rrd'

def generate_rrd_sequence_map(hosts, rrd_map):
    '''
    Example: ((a, dbaux1_mem_free.rrd), (b, ...), ...)
    '''
    rrd_hosts = []
    host_order = []
    for host in hosts:
        for rrd in rrd_map:
            rrd_hosts.append(
                generate_rrd_filename(host, rrd))
            host_order.append(host)

    sequence = []
    it = iter(alphaenum(rrd_hosts))
    for h in host_order:
        char, host = it.next()
        sequence.append((char, host, h))

    return tuple(sequence)

def generate_index():
    run_ssh_command('root@graphs',
            'cd /var/drraw/saved && ./generate_index.py')

def grab_new_drraw(graph):
    command = 'cd /var/drraw/saved && ./grab_drraw_graph.py '
    command += ' '.join([graph.name, graph.filename])
    run_ssh_command('root@graph_server', command)
