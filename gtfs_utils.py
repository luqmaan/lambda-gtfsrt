import arrow
import requests
from google.transit import gtfs_realtime_pb2 as gtfsrt
from protobuf_to_dict import protobuf_to_dict


def get_feed(url, cleanup=False):
    res = requests.get(url)
    feed = feed_from_string(res.content)

    if cleanup:
        return cleanup_feed(feed)

    return feed


def feed_from_string(raw):
    feed = gtfsrt.FeedMessage()
    feed.ParseFromString(raw)
    return feed


def cleanup_feed(feed):
    trip_ids = []
    dupes = []

    for entity in feed.entity:
        if entity.vehicle and entity.vehicle.ByteSize() > 0:
            trip_id = entity.vehicle.trip.trip_id

            if trip_id not in trip_ids:
                trip_ids.append(trip_id)
            elif entity.vehicle:
                dupes.append(entity)

    for entity in dupes:
        feed.entity.remove(entity)

    return feed


def feed_to_dict(feed):
    return protobuf_to_dict(feed)
