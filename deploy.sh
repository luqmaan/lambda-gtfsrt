#!/usr/bin/env bash

set -e
set -x

./build.sh

aws lambda update-function-code \
--function-name gtfsrt-debug \
--zip-file fileb://bundle.zip \
--publish
