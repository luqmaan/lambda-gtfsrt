#!/usr/bin/env python
import io

import requests
from google.transit import gtfs_realtime_pb2 as gtfsrt

from flask import Flask, send_file
app = Flask(__name__)


@app.route("/dedupe")
def dedupe():
    url = 'https://data.texas.gov/download/eiei-9rpf/application/octet-stream'
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

    for entity in dupes:
        feed.entity.remove(entity)

    return send_file(io.BytesIO(feed.SerializeToString()))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6996, debug=True)
