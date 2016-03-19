#!/usr/bin/env python

import json
from unittest import TestCase

import arrow
from mock import patch

import gtfs_utils


class TestGTFSUtils(TestCase):

    maxDiff = None

    @patch('arrow.now', new=lambda: arrow.get(1458167065))
    def test_trip_updates_cst_cdt(self):
        with open('fixtures/cst-cdt-error/trip-updates.pb', 'rb') as fh:
            raw = fh.read()

        feed = gtfs_utils.cleanup_feed(gtfs_utils.feed_from_string(raw))
        actual = gtfs_utils.feed_to_dict(feed)

        with open('fixtures/cst-cdt-error/trip-updates-clean.json') as fh:
            expected = json.loads(fh.read())

        self.assertDictEqual(actual, expected)

    @patch('arrow.now', new=lambda: arrow.get(1458167065))
    def test_vehicle_positions_cst_cdt(self):
        with open('fixtures/cst-cdt-error/vehicle-positions.pb', 'rb') as fh:
            raw = fh.read()

        feed = gtfs_utils.cleanup_feed(gtfs_utils.feed_from_string(raw))
        actual = gtfs_utils.feed_to_dict(feed)

        with open('fixtures/cst-cdt-error/vehicle-positions-clean.json') as fh:
            expected = json.loads(fh.read())

        self.assertDictEqual(actual, expected)
