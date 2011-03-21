#!/usr/bin/python
import sys
import subprocess

name = sys.argv[1]
filename = sys.argv[2]
url = 'https://nodetraq.yourdomain/graphs/rrd_file/' + name

subprocess.call(['curl', '-u', 'nodetraq_username:nodetraq_password', url, '-o', filename])

