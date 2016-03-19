#!/usr/bin/env python

from gtfs_utils import get_feed, feed_to_dict


def lambda_handler(event, ctx):
    url = event.get('url')
    cleanup = event.get('cleanup')

    if url:
        feed = get_feed(url, cleanup)
        return feed_to_dict(feed)
    else:
        return {'error_message': 'Requires the `url` param'}
