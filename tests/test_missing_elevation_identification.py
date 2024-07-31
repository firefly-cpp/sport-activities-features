import os
from unittest import TestCase
from unittest.mock import patch, MagicMock
from sport_activities_features import ElevationIdentification, ElevationApiType
import json

class TestMissingElevationIdentification(TestCase):
    def setUp(self):
        self.positions = [(37.4219999, -122.0840575), (36.778259, -119.417931), (34.052235, -118.243683)]
        self.open_elevation_api = ElevationIdentification(positions=self.positions,
                                                          elevation_api_type=ElevationApiType.OPEN_ELEVATION_API)
        self.open_topo_data_api = ElevationIdentification(positions=self.positions,
                                                          elevation_api_type=ElevationApiType.OPEN_TOPO_DATA_API)

    @patch('http.client.HTTPSConnection')
    def test_fetch_elevation_data_open_elevation_api(self, MockHTTPSConnection):

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "results": [
                     {"latitude": 37.422, "longitude":-122.084058,"elevation":9.0},
                     {"elevation":147.0,"longitude":-119.417931,"latitude":36.778259},
                     {"latitude":34.052235,"longitude":-118.243683,"elevation":102.0}
                 ]
        }).encode('utf-8')

        mock_response.getresponse.return_value = mock_response
        MockHTTPSConnection.return_value = mock_response

        elevations = self.open_elevation_api.fetch_elevation_data()
        self.assertEqual(len(elevations),
                         len(self.positions))  # Check if number of elevations matches number of positions

        self.assertEqual(elevations[0], 9)
        self.assertEqual(elevations[1], 147)
        self.assertEqual(elevations[2], 102)

    @patch('http.client.HTTPSConnection')
    def test_fetch_elevation_data_open_topo_data_api(self, MockHTTPSConnection):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            'results': [
                {'elevation': 8, 'location': {'lat': 39.7391536, 'lng': -104.9847034}},
                {'elevation': 147, 'location': {'lat': 40.748817, 'lng': -73.985428}}
            ]
        }).encode('utf-8')
        mock_response.getresponse.return_value = mock_response

        MockHTTPSConnection.return_value = mock_response

        elevations = self.open_topo_data_api.fetch_open_topo_data()

        expected_elevations = [8, 147]
        self.assertEqual(elevations, expected_elevations)
