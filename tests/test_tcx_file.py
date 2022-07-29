import os
from unittest import TestCase

from sport_activities_features import TCXFile


class TestTCXFile(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.read_one_file(filename)

    def test_total_distance(self):
        self.assertAlmostEqual(self.data['total_distance'], 116366.98, 2)

    def test_number_of_positions(self):
        self.assertEqual(len(self.data['positions']), 7799)

    def test_heartrates(self):
        self.assertEqual(self.data['heartrates'][0], 94)
        self.assertEqual(self.data['heartrates'][1], 95)


# test sup activity
class TestSupTCXFile(TestCase):
    def setUp(self):
	# test file is taken from https://github.com/firefly-cpp/tcx-test-files
        filename = os.path.join(os.path.dirname(__file__), 'data', 'sup_activity_1.tcx')
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.read_one_file(filename)

    def test_total_steps(self):
        self.assertEqual(self.data['steps'], 491)
