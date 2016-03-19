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


def better_timestamp(timestamp):
    time = arrow.get(timestamp)
    now = arrow.now()
    # handle the case where they forgot to change to CDT
    if ((time - now).total_seconds() / 60) > 50:
        return time.replace(hours=-1).timestamp

    return time.timestamp


def cleanup_feed(feed):
    trip_ids = []
    dupes = []

    feed.header.timestamp = better_timestamp(feed.header.timestamp)

    for entity in feed.entity:
        if entity.vehicle and entity.vehicle.ByteSize() > 0:
            trip_id = entity.vehicle.trip.trip_id
            entity.vehicle.timestamp = better_timestamp(entity.vehicle.timestamp)
            if trip_id not in trip_ids:
                trip_ids.append(trip_id)
            elif entity.vehicle:
                dupes.append(entity)

        if entity.trip_update and entity.trip_update.ByteSize() > 0:
            entity.trip_update.timestamp = better_timestamp(entity.trip_update.timestamp)
            for stop_time_update in entity.trip_update.stop_time_update:
                stop_time_update.arrival.time = better_timestamp(stop_time_update.arrival.time)
                stop_time_update.departure.time = better_timestamp(stop_time_update.arrival.time)

    for entity in dupes:
        feed.entity.remove(entity)

    return feed


def feed_to_dict(feed):
    return protobuf_to_dict(feed)
