from __future__ import print_function

import json
import urllib2
from datetime import datetime

LAMBDA_API = 'https://lnykjry6ze.execute-api.us-west-2.amazonaws.com/prod/gtfsrt-debug'
GTFSRT_FEED = 'https://data.texas.gov/download/eiei-9rpf/application/octet-stream'
CRONITOR = '...'


def should_alert(data, url):
    date = datetime.now()
    now = date.isoformat()

    if len(data['entity']) > 0:
        print('{} - SUCCESS - vehicle positions is NOT empty, url: {}'.format(now, url))
        return False

    if date.hour >= 5 and date.hour <= 13:
        print('{} - IGNORED - vehicle positions is empty, but IGNORED because hour is {}, url: {}'.format(now, date.hour, url))
        return False

    print('{} - FAILURE - vehicle positions is empty, url: {}'.format(now, url))

    return True


def lambda_handler(event, context):
    url = '{}?url={}'.format(LAMBDA_API, GTFSRT_FEED)
    res = urllib2.urlopen(url)
    data = json.load(res)

    print('*********************************')
    if should_alert(data, url):
        urllib2.urlopen(CRONITOR)
    print('*********************************')
