import os
from unittest import TestCase

from sport_activities_features import TCXFile


class TestTCXFile(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "15.tcx")
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.read_one_file(filename)

    def test_total_distance(self):
        self.assertAlmostEqual(self.data["total_distance"], 116366.98, 2)

    def test_number_of_positions(self):
        self.assertEqual(len(self.data["positions"]), 7799)

    def test_heartrates(self):
        self.assertEqual(self.data["heartrates"][0], 94)
        self.assertEqual(self.data["heartrates"][1], 95)


# test sup activity
class TestSupTCXFile(TestCase):
    def setUp(self):
        # test file is taken from https://github.com/firefly-cpp/tcx-test-files
        filename = os.path.join(
            os.path.dirname(__file__), "data", "sup_activity_1.tcx"
        )
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.extract_integral_metrics(filename)

    def test_total_steps(self):
        self.assertEqual(self.data["steps"], 491)


# test swimming activity
class TestSwimmingTCXFile(TestCase):
    def setUp(self):
        # test file is taken from https://github.com/firefly-cpp/tcx-test-files
        filename = os.path.join(
            os.path.dirname(__file__), "data", "swimming_activity_1.tcx"
        )
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.extract_integral_metrics(filename)

    def test_total_calories(self):
        self.assertEqual(self.data["calories"], 284)

    def test_total_distance(self):
        self.assertEqual(self.data["distance"], 1330.32)


# test cross-country-skiing activity
class TestCrossCountryTCXFile(TestCase):
    def setUp(self):
        # test file is taken from https://github.com/firefly-cpp/tcx-test-files
        filename = os.path.join(
            os.path.dirname(__file__),
            "data",
            "cross-country-skiing_activity_1.tcx",
        )
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.extract_integral_metrics(filename)

    def test_total_calories(self):
        self.assertEqual(self.data["calories"], 532)

    def test_total_distance(self):
        self.assertEqual(self.data["distance"], 5692.01)


# test walking activity
class TestWalkingTCXFile(TestCase):
    def setUp(self):
        # test file is taken from https://github.com/firefly-cpp/tcx-test-files
        filename = os.path.join(
            os.path.dirname(__file__), "data", "walking_activity_1.tcx"
        )
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.extract_integral_metrics(filename)

    def test_total_calories(self):
        self.assertEqual(self.data["calories"], 329)

    def test_total_distance(self):
        self.assertEqual(self.data["distance"], 3988.82)


# test pool swim activity
class TestPoolSwimmingTCXFile(TestCase):
    def setUp(self):
        # test file is taken from https://github.com/firefly-cpp/tcx-test-files
        filename = os.path.join(
            os.path.dirname(__file__), "data", "pool_swim-activity_1.tcx"
        )
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.extract_integral_metrics(filename)

    def test_total_calories(self):
        self.assertEqual(self.data["calories"], 329)

    def test_total_distance(self):
        self.assertEqual(self.data["distance"], 1500)
