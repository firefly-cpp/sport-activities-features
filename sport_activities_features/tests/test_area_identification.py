import numpy as np
import os
from unittest import TestCase
from sport_activities_features.area_identification import AreaIdentification
from sport_activities_features.tcx_manipulation import TCXFile


class TestAreaIdentification(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        tcx_file = TCXFile()
        self.activity = tcx_file.read_one_file(filename)

        # Converting the read data to arrays.
        positions = np.array([*self.activity['positions']])
        distances = np.array([*self.activity['distances']])
        timestamps = np.array([*self.activity['timestamps']])
        heartrates = np.array([*self.activity['heartrates']])
        area_coordinates = np.array([[[45.445539, 13.736101], [45.566894, 13.700517], [45.563605, 13.806872], [45.480111, 13.812463]]])

        area = AreaIdentification(positions, distances, timestamps, heartrates, area_coordinates)
        area.identify_points_in_area()
        self.data = area.extract_data_in_area()

    def test_distance_correct(self):
        self.assertAlmostEqual(self.data['distance'], 10267.90, places=2)

    def test_time_correct(self):
        self.assertAlmostEqual(self.data['time'], 1470.0, places=1)

    def test_average_speed_correct(self):
        self.assertAlmostEqual(self.data['average_speed'], 6.98, places=2)

    def test_minimum_heart_rate_correct(self):
        self.assertAlmostEqual(self.data["minimum_heart_rate"], 114.0, places=1)

    def test_max_heart_rate_correct(self):
        self.assertAlmostEqual(self.data['maximum_heart_rate'], 171.0, places=1)

    def test_avg_heart_rate_correct(self):
        self.assertAlmostEqual(self.data["average_heart_rate"], 139.0, places=1)
