#!/usr/bin/env python2.6
import sys
import os

from couchdbhelper import CouchHelper

job_folder = sys.path[0]
view_folder = os.path.normpath(
        os.path.join(job_folder, "../model/views"))

ch = CouchHelper("http://localhost:5984")
ch.select("nodetraq")
ch.sync_view(view_folder)

