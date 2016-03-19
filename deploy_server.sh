#!/usr/bin/env bash

set -e
set -x

sudo apt-get update
sudo apt-get install build-essential checkinstall
sudo add-apt-repository ppa:fkrull/deadsnakes-python2.7
sudo apt-get install python2.7
sudo apt-get install python-pip
sudo apt-get install python-virtualenv

virtualenv .env
. .env/bin/activate
pip install -r requirements-server.txt

echo "start on runlevel [2345]
stop on runlevel [016]

respawn
exec " > /etc/init/gtfsrt-server.conf
