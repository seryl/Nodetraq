import subprocess
from datetime import datetime
from time import time, mktime

from sshwrapper import run_ssh_command
from nagiosreader import NagiosReader

print_loc = '/usr/bin/printf'
nagios_loc = '/var/log/nagios/rw/nagios.cmd'
master_server = 'root@nagios1'
nagios2 = 'root@nagios2'
nagios3 = 'root@nagios3'

def nagios_current_time():
    current_time = datetime.now()
    return str(current_time.strftime(
            "%m/%d/%Y %I:%M %p").lower())

def unix_timestamp():
    return int(time())

def webtime_to_timestamp(webtime):
    timestamp_time = datetime.strptime(
        webtime, "%m/%d/%Y %I:%M %p").timetuple()
    return mktime(timestamp_time)

def schedule_host_downtime(
    hostname='', start_time=str(unix_timestamp()),
    end_time='', fixed_trigger_id=0,
    author='', comment=''):
    if not (hostname and end_time and author and comment):
        return False

    if start_time.isdigit():
        start_time = int(start_time)
    else:
        start_time = int(webtime_to_timestamp(start_time))
    if not end_time:
        end_time = start_time + 100000;
    else:
        end_time = int(webtime_to_timestamp(end_time))
    duration = end_time - start_time

    command = print_loc + ' "[%s] ' % unix_timestamp()
    command += 'SCHEDULE_HOST_DOWNTIME'
    command = ';'.join(
        [command, hostname, str(start_time), str(end_time), str(0),
         str(fixed_trigger_id), str(duration), author, comment])
    command += '\\n" > %s' % nagios_loc

    run_ssh_command(master_server, command)
    return True

def enable_host_service_notifications(hostname):
    if not hostname:
        return None

    command = print_loc + ' "[%s] ' % unix_timestamp()
    command += 'ENABLE_HOST_SVC_NOTIFICATIONS'
    command = ';'.join(
        [command, hostname])
    command += '\\n" > %s' % nagios_loc

    run_ssh_command(master_server, command)

    command = print_loc + ' "[%s] ' % unix_timestamp()
    command += 'ENABLE_HOST_NOTIFICATIONS'
    command = ';'.join(
        [command, hostname])
    command += '\\n" > %s' % nagios_loc

    run_ssh_command(master_server, command)
    return True

def disable_host_service_notifications(hostname):
    if not hostname:
        return None

    command = print_loc + ' "[%s] ' % unix_timestamp()
    command += 'DISABLE_HOST_SVC_NOTIFICATIONS'
    command = ';'.join(
        [command, hostname])
    command += '\\n" > %s' % nagios_loc

    run_ssh_command(master_server, command)

    command = print_loc + ' "[%s] ' % unix_timestamp()
    command += 'DISABLE_HOST_NOTIFICATIONS'
    command = ';'.join(
        [command, hostname])
    command += '\\n" > %s' % nagios_loc

    run_ssh_command(master_server, command)
    return True

def acknowledge_svc_problem(hostname='', service=''):
    command = print_loc + ' "[%s] ' % unix_timestamp()
    command += 'ACKNOWLEDGE_SVC_PROBLEM'
    command = ';'.join(
            [command, hostname, service, '1', '1', '0', 'nodetraq', 'acknowledgeded via email'])
    command += '\\n" > %s' % nagios_loc

    run_ssh_command(master_server, command)
    return True


def acknowledge_host_problem(hostname=''):
    command = print_loc + ' "[%s] ' % unix_timestamp()
    command += 'ACKNOWLEDGE_HOST_PROBLEM'
    command = ';'.join(
            [command, hostname, '1', '1', '0', 'nodetraq', 'acknowledgeded via email'])
    command += '\\n" > %s' % nagios_loc

    run_ssh_command(master_server, command)
    return True

def remove_nagios_monitors(hostname):
    fqdn = hostname + '.yourdomain'
    rm = '/bin/rm -rf'
    auto_dir = '/etc/nagios/AUTO/'
    auto_dir += fqdn
    command = rm + " " + auto_dir

    run_ssh_command(master_server, command)
    run_ssh_command(nagios2, command)
    run_ssh_command(nagios3, command)
    return True

def remove_from_downtime(hostname):
    nr = NagiosReader()
    downtimes = nr.parse_downtimes()
    if downtimes:
        down_id = [h for h in downtimes if h["Host Name"] == hostname]
        if down_id:
            # Run removal
            command = print_loc + ' "[%s] ' % unix_timestamp()
            command += 'DEL_HOST_DOWNTIME'
            command = ';'.join(
                    [command, down_id[0]["Downtime ID"]])
            command += '\\n" > %s' % nagios_loc
            run_ssh_command(master_server, command)
        return True
    else:
        return False

