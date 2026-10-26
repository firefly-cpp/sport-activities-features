import os
from datetime import datetime, timedelta
from unittest import TestCase

from tcxreader.tcxreader import TCXExercise, TCXTrackPoint

from sport_activities_features import TCXFile


class TestTCXFile(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        self.tcx_file = TCXFile()
        tcx_exercise = self.tcx_file.read_one_file(filename)
        self.data = self.tcx_file.extract_activity_data(tcx_exercise)

    def test_total_distance(self):
        self.assertAlmostEqual(self.data['total_distance'], 116366.98, 2)

    def test_number_of_positions(self):
        assert len(self.data['positions']) == 7799

    def test_heartrates(self):
        assert self.data['heartrates'][0] == 94
        assert self.data['heartrates'][1] == 95


class TestTCXFileSameTimestamps(TestCase):
    """dead_end.tcx is a planned route: all trackpoints share one timestamp."""

    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__), 'data', 'dead_end.tcx',
        )
        self.tcx_file = TCXFile()
        self.exercise = self.tcx_file.read_one_file(filename)
        self.data = self.tcx_file.extract_activity_data(self.exercise)

    def test_all_trackpoints_are_kept(self):
        self.assertEqual(len(self.exercise.trackpoints), 48)
        for key in (
            'positions', 'altitudes', 'distances', 'timestamps',
            'heartrates', 'speeds',
        ):
            self.assertEqual(len(self.data[key]), 48, key)

    def test_route_ends_at_its_last_trackpoint(self):
        last = self.exercise.trackpoints[-1]
        self.assertEqual(
            self.data['positions'][-1], (last.latitude, last.longitude),
        )
        self.assertEqual(self.data['distances'][-1], last.distance)

    def test_speeds(self):
        # The first 47 trackpoints share one timestamp, the last one is
        # an hour later.
        self.assertEqual(self.data['speeds'][:47], [0] * 47)
        trackpoints = self.exercise.trackpoints
        self.assertAlmostEqual(
            self.data['speeds'][-1],
            (trackpoints[-1].distance - trackpoints[-2].distance) / 3600 * 3.6,
        )


def make_exercise(points):
    return TCXExercise(
        trackpoints=[
            TCXTrackPoint(
                latitude=46.0, longitude=15.0, elevation=200.0,
                time=time, distance=distance,
            )
            for time, distance in points
        ],
    )


class TestTCXFileSpeeds(TestCase):
    start = datetime(2026, 1, 1, 10, 0, 0)

    def extract(self, points):
        return TCXFile().extract_activity_data(make_exercise(points))

    def test_speed(self):
        data = self.extract([
            (self.start, 0),
            (self.start + timedelta(seconds=10), 100),
        ])
        self.assertEqual(data['speeds'], [0, 36.0])

    def test_same_timestamp_keeps_point_and_previous_speed(self):
        data = self.extract([
            (self.start, 0),
            (self.start + timedelta(seconds=10), 100),
            (self.start + timedelta(seconds=10), 105),
            (self.start + timedelta(seconds=20), 205),
        ])
        self.assertEqual(data['distances'], [0, 100, 105, 205])
        self.assertEqual(data['speeds'], [0, 36.0, 36.0, 36.0])

    def test_missing_time_or_distance(self):
        data = self.extract([
            (self.start, None),
            (None, 50),
            (self.start + timedelta(seconds=10), None),
            (self.start + timedelta(seconds=20), 200),
        ])
        self.assertEqual(data['distances'], [0, 50, None, 200])
        self.assertEqual(data['speeds'], [0, None, None, None])

    def test_no_trackpoints(self):
        data = self.extract([])
        self.assertEqual(data['positions'], [])
        self.assertEqual(data['speeds'], [])
