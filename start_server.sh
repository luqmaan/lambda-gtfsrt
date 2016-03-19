#!/usr/bin/env bash

set -e
set -x

source /var/www/lambda-gtfsrt/.env/bin/activate
python /var/www/lambda-gtfsrt/server.py
