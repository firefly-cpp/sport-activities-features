import contextlib
import io
import math
import os
from unittest import TestCase

import numpy as np

from sport_activities_features.dead_end_identification import (
    DeadEndIdentification,
)
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.tcx_manipulation import TCXFile

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
EARTH_RADIUS = 6371008.8
LATITUDE, LONGITUDE = 46.0, 15.0


def route(xy, distance_scale=1.0):
    """(positions, cumulative distances) of a route given in meters
    around (46 N, 15 E). distance_scale stretches the recorded distances
    of the second half, like a device that measures the way back a bit
    differently."""
    xy = np.asarray(xy, dtype=float)
    latitudes = LATITUDE + np.degrees(xy[:, 1] / EARTH_RADIUS)
    longitudes = LONGITUDE + np.degrees(
        xy[:, 0] / (EARTH_RADIUS * math.cos(math.radians(LATITUDE))),
    )
    steps = np.hypot(*np.diff(xy, axis=0).T)
    steps[len(steps) // 2:] *= distance_scale
    distances = np.concatenate([[0.0], np.cumsum(steps)])
    return list(zip(latitudes, longitudes)), list(distances)


def straight(start, end, step=5.0):
    start, end = np.asarray(start, float), np.asarray(end, float)
    n = max(int(np.hypot(*(end - start)) / step), 1)
    return [start + (end - start) * i / n for i in range(n + 1)]


def out_and_back(length, lateral_noise=0.0, seed=0):
    """Approach 1 km east, go length m north and back, leave 1 km east."""
    rng = np.random.default_rng(seed)
    points = straight((-1000, 0), (0, 0))
    points += straight((0, 0), (0, length))[1:]
    points += straight((3, length), (3, 0))[1:]  # way back 3 m beside
    points += straight((3, 0), (1000, 0))[1:]
    points = np.array(points)
    points += rng.normal(0, lateral_noise, points.shape)
    return points


def identify(positions, distances, **kwargs):
    dead_ends = DeadEndIdentification(positions, distances, **kwargs)
    dead_ends.identify_dead_ends()
    return dead_ends


def spans(dead_ends):
    """Dead ends as (start, end) in meters of distance."""
    return [
        (dead_ends.distances[s], dead_ends.distances[e])
        for s, e in dead_ends.dead_ends
    ]


class TestDeadEndsInActivities(TestCase):
    def load(self, name):
        reader = TCXFile() if name.endswith('.tcx') else GPXFile()
        activity = reader.extract_activity_data(
            reader.read_one_file(os.path.join(DATA_DIR, name)),
        )
        return identify(activity['positions'], activity['distances'])

    def test_planned_route_with_dead_end(self):
        # dead_end.tcx goes out from 5707 m, turns at 6612 m and is back
        # at the same place at 7515 m.
        found = spans(self.load('dead_end.tcx'))
        self.assertEqual(len(found), 1)
        start, end = found[0]
        self.assertAlmostEqual(start, 5707, delta=50)
        self.assertAlmostEqual(end, 7515, delta=50)
        self.assertAlmostEqual((start + end) / 2, 6612, delta=10)

    def test_ride_with_long_spur(self):
        # 15.tcx has a spur of about 6 km to the north and back.
        found = spans(self.load('15.tcx'))
        self.assertEqual(len(found), 1)
        start, end = found[0]
        self.assertGreater((end - start) / 2, 5000)

    def test_rides_without_dead_ends(self):
        for name in ('2.tcx', '11.tcx', 'broken1.gpx'):
            with self.subTest(name):
                self.assertEqual(len(self.load(name).dead_ends), 0)


class TestDeadEndIdentification(TestCase):
    def test_out_and_back(self):
        points = out_and_back(1000, lateral_noise=2)
        positions, distances = route(points)
        found = spans(identify(positions, distances))
        self.assertEqual(len(found), 1)
        start, end = found[0]
        # The noise makes the recorded distances longer than the geometry,
        # so compare with the recorded distance at the foot of the spur
        # (the 201st point, on the way out and on the way back).
        foot_out = distances[200]
        foot_back = distances[len(points) - 201]
        self.assertAlmostEqual(start, foot_out, delta=60)
        self.assertAlmostEqual(end, foot_back, delta=60)

    def test_distance_measured_differently_on_the_way_back(self):
        # The way back is recorded 2 % longer: the mirrored points drift
        # 20 m apart over 1 km, which the U-turn allowance absorbs.
        positions, distances = route(out_and_back(1000), distance_scale=1.02)
        found = spans(identify(positions, distances))
        self.assertEqual(len(found), 1)
        start, end = found[0]
        self.assertGreater(end - start, 1800)

    def test_too_short(self):
        positions, distances = route(out_and_back(300))
        self.assertEqual(len(identify(positions, distances).dead_ends), 0)
        self.assertEqual(
            len(identify(
                positions, distances, minimum_distance=200,
            ).dead_ends),
            1,
        )

    def test_loop_is_not_a_dead_end(self):
        angles = np.linspace(0, 2 * math.pi, 400)
        circle = np.column_stack([300 * np.cos(angles), 300 * np.sin(angles)])
        positions, distances = route(circle)
        self.assertEqual(len(identify(positions, distances).dead_ends), 0)

    def test_way_back_on_a_parallel_road(self):
        # Back on a road 60 m away: not the same path.
        points = straight((0, 0), (0, 1000))
        points += straight((60, 1000), (60, 0))
        positions, distances = route(points)
        self.assertEqual(len(identify(positions, distances).dead_ends), 0)

    def test_two_dead_ends(self):
        points = list(out_and_back(800))
        second = out_and_back(800) + np.array([3000, 0])
        points += list(second)
        positions, distances = route(points)
        self.assertEqual(len(identify(positions, distances).dead_ends), 2)

    def test_missing_values_and_no_data(self):
        positions, distances = route(out_and_back(1000))
        positions[10] = None
        distances[20] = None
        self.assertEqual(len(identify(positions, distances).dead_ends), 1)
        self.assertEqual(len(identify([], []).dead_ends), 0)

    def test_no_output_and_deprecated_degrees(self):
        positions, distances = route(out_and_back(1000))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            identify(positions, distances)
        self.assertEqual(output.getvalue(), '')
        with self.assertWarns(DeprecationWarning):
            DeadEndIdentification(positions, distances, tolerance_degrees=5)

    def test_identify_returns_dead_ends(self):
        positions, distances = route(out_and_back(1000))
        dead_ends = DeadEndIdentification(positions, distances)
        result = dead_ends.identify_dead_ends()
        self.assertIs(result, dead_ends.dead_ends)
        self.assertEqual(result.shape, (1, 2))
