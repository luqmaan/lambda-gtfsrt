#!/usr/bin/env python

import io

from flask import Flask, send_file, Response, request, jsonify

from gtfs_utils import get_feed, feed_to_dict

app = Flask(__name__)


@app.route("/protobuf")
def protobuf():
    url = request.args.get('url')
    cleanup = request.args.get('cleanup')
    feed = get_feed(url, cleanup)

    return send_file(io.BytesIO(feed.SerializeToString()))


@app.route("/human")
def human():
    url = request.args.get('url')
    cleanup = request.args.get('cleanup')
    feed = get_feed(url, cleanup)

    return Response(str(feed), mimetype='text')


@app.route("/json")
def json():
    url = request.args.get('url')
    cleanup = request.args.get('cleanup')
    feed = get_feed(url, cleanup)

    return jsonify(feed_to_dict(feed))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6996, debug=False)
