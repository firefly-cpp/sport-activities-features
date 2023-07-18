import os
from unittest import TestCase

from tcxreader.tcxreader import TCXReader


class TestTCXReader(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        self.tcx = TCXReader().read(filename)

    def test_distance(self):
        assert self.tcx.distance == 116366.98

    def test_duration(self):
        assert self.tcx.duration == 17250.0

    def test_calories(self):
        assert self.tcx.calories == 2010

    def test_hr_avg(self):
        assert int(self.tcx.hr_avg) == 140

    def test_hr_max(self):
        assert self.tcx.hr_max == 200

    def test_hr_min(self):
        assert self.tcx.hr_min == 94

    def altitude_avg(self):
        assert self.tcx.altitude_avg is None

    def test_altitude_min(self):
        self.assertAlmostEqual(self.tcx.altitude_min, -5.4, places=1)

    def test_ascent(self):
        self.assertAlmostEqual(self.tcx.ascent, 1404.4, places=1)

    def test_descent(self):
        self.assertAlmostEqual(self.tcx.descent, 1422.0, places=1)
