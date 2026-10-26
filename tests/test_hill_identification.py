import math
import os
from unittest import TestCase

import geopy.distance
import pytest

from sport_activities_features.hill_identification import (
    HillIdentification,
)
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures


def identify(altitudes, distances=None, ascent_threshold=30):
    hill = HillIdentification(
        altitudes, distances, ascent_threshold=ascent_threshold,
    )
    hill.identify_hills()
    return hill


class TestHillIdentificationActivity(TestCase):
    """Regression values for a real activity (tests/data/15.tcx)."""

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "15.tcx")
        tcx_file = TCXFile()
        tcx_exercise = tcx_file.read_one_file(filename)
        self.activity = tcx_file.extract_activity_data(tcx_exercise)
        self.hill = HillIdentification(
            self.activity["altitudes"],
            self.activity["distances"],
            ascent_threshold=30,
        )
        self.hill.identify_hills()
        self.hills = self.hill.return_hills()
        self.top = TopographicFeatures(self.hills)

    def test_hills(self):
        self.assertEqual(
            self.hills,
            [
                [18, 283], [801, 1819], [2431, 3306], [3459, 4134],
                [4801, 5658], [6444, 6643], [7238, 7556],
            ],
        )

    def test_every_hill_is_a_climb_above_threshold(self):
        altitudes = self.activity["altitudes"]
        for stored in self.hill.identified_hills:
            start, end = stored.segment
            self.assertGreaterEqual(altitudes[end] - altitudes[start], 30)
            self.assertAlmostEqual(
                stored.ascent, altitudes[end] - altitudes[start],
            )

    def test_num_hills_correct(self):
        self.assertEqual(self.top.num_of_hills(), 7)

    def test_total_ascent_matches_tcx(self):
        self.assertAlmostEqual(self.hill.total_ascent, 1404.4, places=1)
        self.assertAlmostEqual(self.hill.total_descent, 1422.0, places=1)

    def test_avg_altitude_correct(self):
        self.assertAlmostEqual(
            self.top.avg_altitude_of_hills(self.activity["altitudes"]),
            113.998,
            places=2,
        )

    def test_avg_ascent_correct(self):
        self.assertAlmostEqual(
            self.top.avg_ascent_of_hills(self.activity["altitudes"]),
            182.943,
            places=2,
        )

    def test_distance_of_hills_correct(self):
        distance = self.top.distance_of_hills(self.activity["positions"])
        self.assertAlmostEqual(distance, 50.694, places=2)

        # Cross-check against the distances recorded by the device.
        distances = self.activity["distances"]
        recorded = sum(distances[e] - distances[s] for s, e in self.hills)
        self.assertAlmostEqual(distance, recorded / 1000, delta=0.5)

    def test_share_of_hills_correct(self):
        distance_hills = self.top.distance_of_hills(self.activity["positions"])
        self.assertAlmostEqual(
            self.top.share_of_hills(
                distance_hills, self.activity["total_distance"]
            ),
            0.436,
            places=3,
        )

    def test_avg_grade_of_hill(self):
        self.assertAlmostEqual(
            self.hill.identified_hills[0].average_slope, 2.75027, 4
        )

    def test_identify_hills_twice_gives_same_result(self):
        self.hill.identify_hills()
        self.assertEqual(self.hill.return_hills(), self.hills)


class TestHillIdentification(TestCase):
    """Small synthetic profiles with an obvious expected result."""

    def test_single_hill(self):
        hill = identify([0, 10, 20, 30, 40, 30, 20])
        self.assertEqual(hill.return_hills(), [[0, 4]])
        self.assertEqual(hill.identified_hills[0].ascent, 40)

    def test_climb_below_threshold_is_not_a_hill(self):
        self.assertEqual(identify([0, 10, 20, 29, 0]).return_hills(), [])

    def test_descent_is_not_a_hill(self):
        self.assertEqual(identify([100, 80, 50, 0]).return_hills(), [])

    def test_small_climb_at_the_end_is_not_a_hill(self):
        hill = identify([0, 40, 0, 10])
        self.assertEqual(hill.return_hills(), [[0, 1]])

    def test_climb_at_the_end_is_a_hill(self):
        hill = identify([0, 0, 10, 40])
        self.assertEqual(hill.return_hills(), [[1, 3]])

    def test_small_dip_does_not_split_a_hill(self):
        hill = identify([0, 40, 25, 60, 0])
        self.assertEqual(hill.return_hills(), [[0, 3]])
        self.assertEqual(hill.identified_hills[0].ascent, 60)

    def test_large_dip_splits_hills(self):
        hill = identify([0, 40, 5, 50, 0])
        self.assertEqual(hill.return_hills(), [[0, 1], [2, 3]])

    def test_flat_ground_before_climb_is_not_part_of_hill(self):
        hill = identify([0, 0.5, 0, 0.3, 0.8, 10, 40])
        self.assertEqual(hill.return_hills(), [[4, 6]])

    def test_threshold(self):
        self.assertEqual(
            identify([0, 20, 0], ascent_threshold=15).return_hills(),
            [[0, 1]],
        )
        self.assertEqual(
            identify([0, 20, 0], ascent_threshold=25).return_hills(), [],
        )

    def test_missing_altitudes_are_skipped(self):
        hill = identify([0, None, 20, float("nan"), 40, None, 0])
        self.assertEqual(hill.return_hills(), [[0, 4]])
        self.assertEqual(hill.total_ascent, 40)
        self.assertEqual(hill.total_descent, 40)

    def test_too_few_points(self):
        for altitudes in ([], [10], [None, 10]):
            hill = identify(altitudes)
            self.assertEqual(hill.return_hills(), [])
            self.assertEqual(hill.total_ascent, 0)

    def test_total_ascent_and_descent(self):
        hill = identify([0, 10, 5, 20, 0])
        self.assertEqual(hill.total_ascent, 25)
        self.assertEqual(hill.total_descent, 25)

    def test_grade(self):
        hill = identify([0, 30], distances=[0, 300])
        self.assertAlmostEqual(
            hill.identified_hills[0].average_slope,
            math.degrees(math.atan(30 / 300)),
        )

    def test_grade_without_distances(self):
        self.assertIsNone(identify([0, 30]).identified_hills[0].average_slope)

    def test_number_as_distances_warns(self):
        with pytest.warns(UserWarning, match="ascent_threshold"):
            hill = HillIdentification([0, 40, 0], 30)
        hill.identify_hills()
        self.assertEqual(hill.return_hills(), [[0, 1]])
        self.assertIsNone(hill.identified_hills[0].average_slope)


class TestTopographicFeatures(TestCase):
    # Points 0.001° of latitude apart along a meridian (~111 m each).
    positions = [(46.0 + i * 0.001, 15.0) for i in range(6)]
    altitudes = [0, 10, 40, 20, 50, 0]

    def step(self, i):
        return geopy.distance.geodesic(
            self.positions[i], self.positions[i + 1],
        ).km

    def test_distance_of_hills_uses_all_points_of_each_hill(self):
        top = TopographicFeatures([[0, 2], [3, 4]])
        expected = self.step(0) + self.step(1) + self.step(3)
        self.assertAlmostEqual(
            top.distance_of_hills(self.positions), expected,
        )

    def test_avg_altitude_uses_all_points_of_each_hill(self):
        top = TopographicFeatures([[0, 2], [3, 4]])
        self.assertAlmostEqual(
            top.avg_altitude_of_hills(self.altitudes),
            ((0 + 10 + 40) / 3 + (20 + 50) / 2) / 2,
        )

    def test_avg_ascent(self):
        top = TopographicFeatures([[0, 4]])
        self.assertEqual(top.avg_ascent_of_hills(self.altitudes), 70)

    def test_share_of_hills(self):
        top = TopographicFeatures([])
        self.assertAlmostEqual(top.share_of_hills(2.5, 10000), 0.25)
        self.assertEqual(top.share_of_hills(2.5, 0), 0)

    def test_no_hills(self):
        top = TopographicFeatures([])
        self.assertEqual(top.num_of_hills(), 0)
        self.assertEqual(top.distance_of_hills(self.positions), 0)
        self.assertEqual(top.avg_altitude_of_hills(self.altitudes), 0)
        self.assertEqual(top.avg_ascent_of_hills(self.altitudes), 0)
