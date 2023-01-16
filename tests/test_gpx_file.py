import os
from unittest import TestCase

from sport_activities_features import GPXFile


class TestGPXFile(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            'data',
            'riderx3.gpx'
        )
        self.gpx_file = GPXFile()
        self.data = self.gpx_file.read_one_file(filename)

    def test_total_distance(self):
        self.assertAlmostEqual(self.data['total_distance'], 5774.703, 2)

    def test_number_of_positions(self):
        self.assertEqual(len(self.data['positions']), 931)

    def test_heartrates(self):
        self.assertEqual(self.data['heartrates'][0], 107)
        self.assertEqual(self.data['heartrates'][1], 106)

    def test_utf8_formatting(self):
        utf8_filenames = ['broken1.gpx', 'broken2.gpx', 'broken3.gpx', 'broken4.gpx', 'broken5.gpx']
        utf8_distances = [27060.581619705063, 33440.56224468814, 33759.501685168645, 33689.54802374273, 19086.306482072534]
        for index, f in enumerate(utf8_filenames):
            filename = os.path.join(
                os.path.dirname(__file__),
                'data',
                f
            )
            data = self.gpx_file.read_one_file(filename)
            self.assertAlmostEqual(data['total_distance'], utf8_distances[index], places=5)

