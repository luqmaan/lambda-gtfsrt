#!/usr/bin/env python

import arrow
import requests
from google.transit import gtfs_realtime_pb2 as gtfsrt


def parse_vehicle_position(entity):
    v = entity.vehicle

    if v.timestamp != 0:
        return {
            'vehicle_id': int(v.vehicle.id),
            'latitude': v.position.latitude,
            'longitude': v.position.longitude,
            'route_id': int(v.trip.route_id),
            'trip_id': int(v.trip.trip_id),
            'timestamp': arrow.get(v.timestamp).isoformat()
        }


def parse_trip_update(entity):
    tu = entity.trip_update
    st_updates = []
    for stu in tu.stop_time_update:
        st_updates.append({
            'stop_id': stu.stop_id,
            'arrival_time': arrow.get(stu.arrival.time).isoformat(),
            'departure_time': arrow.get(stu.departure.time).isoformat(),
            'delay': stu.departure.delay,
            'uncertainty': stu.departure.uncertainty,
        })

    if st_updates:
        return {
            'timestamp': arrow.get(tu.timestamp).isoformat(),
            'route_id': tu.trip.route_id,
            'trip_id': tu.trip.trip_id,
            'vehicle_id': tu.vehicle.id,
            'stop_time_updates': st_updates
        }


def dedupe(url):
    feed = gtfsrt.FeedMessage()
    res = requests.get(url)
    feed.ParseFromString(res.content)

    trip_ids = []
    dupes = []

    for entity in feed.entity:
        if entity.vehicle:
            trip_id = entity.vehicle.trip.trip_id
            if trip_id not in trip_ids:
                trip_ids.append(trip_id)
                print(trip_id)
            elif entity.vehicle:
                dupes.append(entity)

    print('Deleting dupes', dupes)

    for entity in dupes:
        feed.entity.remove(entity)

    feed.SerializeToString()


def fetch_feed(url):
    feed = gtfsrt.FeedMessage()
    res = requests.get(url)
    feed.ParseFromString(res.content)

    vehicles = []
    updates = []
    for entity in feed.entity:
        vehicle = parse_vehicle_position(entity)
        if vehicle:
            vehicles.append(vehicle)

        trip_update = parse_trip_update(entity)
        if trip_update:
            updates.append(trip_update)

    return {'vehicle_positions': vehicles, 'trip_updates': updates}


def lambda_handler(event, ctx):
    url = event.get('url')
    dedupe = event.get('dedupe')

    if url and dedupe:
        return dedupe(url)
    if url:
        return fetch_feed(url)
    else:
        return {'error_message': 'Requires the `url` param'}

if __name__ == '__main__':
    fetch_feed('https://data.texas.gov/download/eiei-9rpf/application/octet-stream')
