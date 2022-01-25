import os
from unittest import TestCase
from sport_activities_features import GPXFile


class TestGPXFile(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "riderx3.gpx")
        self.gpx_file=GPXFile()
        self.data = self.gpx_file.read_one_file(filename)

    def test_total_distance(self):
        self.assertAlmostEqual(self.data['total_distance'], 5774.703, 2)

    def test_number_of_positions(self):
        self.assertEqual(len(self.data['positions']), 931)

    def test_heartrates(self):
        self.assertEqual(self.data['heartrates'][0], 107)
        self.assertEqual(self.data['heartrates'][1], 106)
