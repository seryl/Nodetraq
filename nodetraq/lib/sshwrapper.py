from subprocess import Popen, PIPE

def run_ssh_command(hostname, command):
    args = ['/usr/bin/ssh', hostname, command]
    p = Popen(args, stdout=PIPE)
    try:
        data = p.communicate()
        p.wait()
        return data
    except Exception as e:
        print e

