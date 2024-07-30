import os
from unittest import TestCase
from sport_activities_features import ElevationIdentification, ElevationApiType  # Make sure to import your class from its module


class TestMissingElevationIdentification(TestCase):
    def setUp(self):
        self.positions = [(37.4219999, -122.0840575), (36.778259, -119.417931), (34.052235, -118.243683)]
        self.open_elevation_api = ElevationIdentification(positions=self.positions,
                                                          elevation_api_type=ElevationApiType.OPEN_ELEVATION_API)
        self.open_topo_data_api = ElevationIdentification(positions=self.positions,
                                                          elevation_api_type=ElevationApiType.OPEN_TOPO_DATA_API)

    def test_fetch_elevation_data_open_elevation_api(self):
        elevations = self.open_elevation_api.fetch_elevation_data()
        self.assertEqual(len(elevations),
                         len(self.positions))  # Check if number of elevations matches number of positions

        self.assertEqual(elevations[0], 9)
        self.assertEqual(elevations[1], 147)
        self.assertEqual(elevations[2], 102)

    def test_fetch_elevation_data_open_topo_data_api(self):
        elevations = self.open_topo_data_api.fetch_elevation_data()
        self.assertEqual(len(elevations),
                         len(self.positions))
        self.assertEqual(elevations[0], 8)
        self.assertEqual(elevations[1], 147)
        self.assertEqual(elevations[2], 93)