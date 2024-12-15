import os
from unittest import TestCase

from sport_activities_features import TCXFile


class TestTCXFile(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        self.tcx_file = TCXFile()
        tcx_exercise = self.tcx_file.read_one_file(filename)
        self.data = self.tcx_file.extract_activity_data(tcx_exercise)

    def test_total_distance(self):
        self.assertAlmostEqual(self.data['total_distance'], 116366.98, 2)

    def test_number_of_positions(self):
        assert len(self.data['positions']) == 7799

    def test_heartrates(self):
        assert self.data['heartrates'][0] == 94
        assert self.data['heartrates'][1] == 95
