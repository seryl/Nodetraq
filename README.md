# Overview

Nodetraq is a server management utility that was put together at RockYou!

This version is stripped of all of the internal specific libraries at RY, however it's still going to take a bit of work to make it completely usable outside.

But there's a strong set of utilities here and without too much work this could become something a little more generic.

Anyone who's interested in this, ping me and maybe we could take it a step further.

# Installation and Setup

## Install ssl libraries
* sudo yum install openssl-devel
* sudo yum install openldap-devel
* sudo yum install sqlite-devel
* sudo yum install sqlite

## Require python 2.6
    Compile it with:
        ./configure
        make altinstall (on older centos boxes)

## Install python2.6 python-setuptools
    python2.6 setup.py install (on the setuptools directory)

## Install the remaining libraries
* sudo easy_install pip
* sudo pip install pylons

## Install the library as an egg

    cd ~/Sites/nodetraq/
    sudo python2.6 setup.py install

## Setup the database

Setup the default nodetraq ini file for production (If you're developing use development.ini instead of production).

    paster setup-app production.ini

## Run the server

Start up the pylons instance by running paster.

    paster serve --reload production.ini --pid=paster.pid --d --monitor-restart

## All set!

Now just browse to http://localhost:5000/ or proxy Apache/nginx there.

