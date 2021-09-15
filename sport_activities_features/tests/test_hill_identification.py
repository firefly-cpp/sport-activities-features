import os
from unittest import TestCase
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures
from sport_activities_features.plot_data import PlotData


class TestHillIdentification(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "15.tcx")
        tcx_file = TCXFile()
        self.activity = tcx_file.read_one_file(filename)
        Hill = HillIdentification(self.activity["altitudes"], 30)
        Hill.identify_hills()
        all_hills = Hill.return_hills()
        self.top = TopographicFeatures(all_hills)

    def test_num_hills_correct(self):
        self.assertEqual(self.top.num_of_hills(), 13)

    def test_avg_altitude_correct(self):
        self.assertAlmostEqual(
            self.top.avg_altitude_of_hills(self.activity["altitudes"]), 145.0, places=1
        )

    def test_avg_ascent_correct(self):
        self.assertAlmostEqual(
            self.top.avg_ascent_of_hills(self.activity["altitudes"]), 91.6, places=1
        )

    def test_distance_of_hills_correct(self):
        self.assertAlmostEqual(
            self.top.distance_of_hills(self.activity["positions"]), 20.0, places=1
        )

    def test_share_of_hills_correct(self):
        distance_hills = self.top.distance_of_hills(self.activity["positions"])
        self.assertAlmostEqual(
            self.top.share_of_hills(distance_hills, self.activity["total_distance"]),
            0.17,
            places=2,
        )
