#!/usr/bin/python
import os
import re
import sys

from urllib import unquote

drraw_regex = re.compile(r"(g|d)\d+.\d+")

def get_directory_files(directory):
    filelist = [
        f for f in os.listdir(directory)\
                if os.path.isfile(
                    os.path.join(directory, f))]
    return filelist

def remove_nondrraw_files(filelist):
    drraw_list = []
    for f in filelist:
        if drraw_regex.search(f):
            drraw_list.append(f)

    return drraw_list

def update_index():
    cwd = os.getcwdu()
    filelist = get_directory_files(cwd)
    filelist = remove_nondrraw_files(filelist)

    index_list = []
    for f in filelist:
        cur_file = open(f)
        data = cur_file.readlines()
        for line in data:
            if line.startswith("gTitle"):
                line = line.replace("gTitle=", "")
                if line:
                    index_list.append(
                        ':'.join(
                         [f, unquote(line.rstrip('\n'))]))
            elif line.startswith("dTitle"):
                line = line.replace("dTitle=", "")
                if line:
                    index_list.append(
                        ':'.join(
                         [f, unquote(line.rstrip('\n'))]))

    return "\n".join(index_list)

def write_index(data):
    f = open("index", "w")
    f.write(data)
    f.close()

if __name__ == '__main__':
    write_index(update_index())

