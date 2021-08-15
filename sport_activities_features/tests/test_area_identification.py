import numpy as np
import os
from unittest import TestCase
from sport_activities_features.area_identification import AreaIdentification
from sport_activities_features.tcx_manipulation import TCXFile


class TestAreaIdentification(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "15.tcx")
        tcx_file = TCXFile()
        self.activity = tcx_file.read_one_file(filename)
        area_coordinates = np.array(
            [
                [[10, 10], [10, 50], [50, 50], [50, 10]],
                [[19, 19], [19, 21], [21, 21], [21, 19]],
            ]
        )
        area = AreaIdentification(
            self.activity["positions"],
            self.activity["distances"],
            self.activity["timestamps"],
            self.activity["heartrates"],
            area_coordinates,
        )
        area.identify_points_in_area()
        self.data = area.extract_data_in_area()

    def test_distance_correct(self):
        self.assertAlmostEqual(self.data["distance"], 116367.0, places=1)

    def test_time_correct(self):
        self.assertAlmostEqual(self.data["time"], 17250.0, places=1)

    def test_max_speed_correct(self):
        self.assertAlmostEqual(self.data["max_speed"], 21.4, places=1)

    def test_avg_speed_correct(self):
        self.assertAlmostEqual(self.data["avg_speed"], 6.7, places=1)

    def test_min_heartrate_correct(self):
        self.assertAlmostEqual(self.data["min_heartrate"], 95.0, places=1)

    def test_max_heartrate_correct(self):
        self.assertAlmostEqual(self.data["max_heartrate"], 200.0, places=1)

    def test_avg_heartrate_correct(self):
        self.assertAlmostEqual(self.data["avg_heartrate"], 140.6, places=1)
