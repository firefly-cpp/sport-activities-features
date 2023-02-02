import os
from unittest import TestCase

from sport_activities_features.hill_identification import (
    HillIdentification,
)
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures


class TestHillIdentification(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "15.tcx")
        tcx_file = TCXFile()
        self.activity = tcx_file.read_one_file(filename)
        self.hill = HillIdentification(
            self.activity["altitudes"], self.activity["distances"], 30
        )
        self.hill.identify_hills()
        all_hills = self.hill.return_hills()
        self.top = TopographicFeatures(all_hills)

    def test_num_hills_correct(self):
        self.assertEqual(self.top.num_of_hills(), 13)

    def test_avg_altitude_correct(self):
        self.assertAlmostEqual(
            self.top.avg_altitude_of_hills(self.activity["altitudes"]),
            145.0,
            places=1,
        )

    def test_avg_ascent_correct(self):
        self.assertAlmostEqual(
            self.top.avg_ascent_of_hills(self.activity["altitudes"]),
            91.6,
            places=1,
        )

    def test_distance_of_hills_correct(self):
        self.assertAlmostEqual(
            self.top.distance_of_hills(self.activity["positions"]),
            20.0,
            places=1,
        )

    def test_share_of_hills_correct(self):
        distance_hills = self.top.distance_of_hills(self.activity["positions"])
        self.assertAlmostEqual(
            self.top.share_of_hills(
                distance_hills, self.activity["total_distance"]
            ),
            0.17,
            places=2,
        )

    def test_avg_grade_of_hill(self):
        self.assertAlmostEqual(
            self.hill.identified_hills[0].average_slope, 2.336246, 5
        )
