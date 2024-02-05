import os
from unittest import TestCase
from sport_activities_features import ElevationIdentification  # Make sure to import your class from its module


class TestMissingElevationIdentification(TestCase):
    def setUp(self):
        self.positions = [(37.4219999, -122.0840575), (36.778259, -119.417931), (34.052235, -118.243683)]
        self.elevation_id = ElevationIdentification(positions=self.positions)

    def test_fetch_elevation_data(self):
        elevations = self.elevation_id.fetch_elevation_data()
        self.assertEqual(len(elevations),
                         len(self.positions))  # Check if number of elevations matches number of positions

        self.assertEqual(elevations[0], 9)
        self.assertEqual(elevations[1], 147)
        self.assertEqual(elevations[2], 102)
