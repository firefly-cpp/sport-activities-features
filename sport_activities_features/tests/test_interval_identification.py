import os
from unittest import TestCase
from sport_activities_features.interval_identification import (
    IntervalIdentificationByPower,
    IntervalIdentificationByHeartrate,
)
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.plot_data import PlotData


class TestHillIdentification(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "2.tcx")
        tcx_file = TCXFile()
        self.activity = tcx_file.read_one_file(filename)

        # Identifying the intervals in the activity by power
        IntervalsPower = IntervalIdentificationByPower(
            self.activity["distances"],
            self.activity["timestamps"],
            self.activity["altitudes"],
            70,
        )
        IntervalsPower.identify_intervals()
        self.statistics_power = IntervalsPower.calculate_interval_statistics()

        # Identifying the intervals in the activity by heart rate
        IntervalsHeartrate = IntervalIdentificationByHeartrate(
            self.activity["distances"],
            self.activity["timestamps"],
            self.activity["altitudes"],
            self.activity["heartrates"],
        )
        IntervalsHeartrate.identify_intervals()
        self.statistics_heartrate = IntervalsHeartrate.calculate_interval_statistics()

    def test_num_intervals_correct(self):
        self.assertEqual(self.statistics_power["number_of_intervals"], 19)
        self.assertEqual(self.statistics_heartrate["number_of_intervals"], 4)

    def test_min_duration_correct(self):
        self.assertAlmostEqual(self.statistics_power["min_duration"], 1.0, places=1)
        self.assertAlmostEqual(
            self.statistics_heartrate["min_duration_interval"], 134.0, places=1
        )

    def test_max_duration_correct(self):
        self.assertAlmostEqual(self.statistics_power["max_duration"], 207.0, places=1)
        self.assertAlmostEqual(
            self.statistics_heartrate["max_duration_interval"], 2191.0, places=1
        )

    def test_avg_duration_correct(self):
        self.assertAlmostEqual(self.statistics_power["avg_duration"], 84.2, places=1)
        self.assertAlmostEqual(
            self.statistics_heartrate["avg_duration_interval"], 829.75, places=2
        )

    def test_min_distance_correct(self):
        self.assertAlmostEqual(self.statistics_power["min_distance"], 6.8496, places=4)
        self.assertAlmostEqual(
            self.statistics_heartrate["min_distance_interval"], 794.83, places=2
        )

    def test_max_distance_correct(self):
        self.assertAlmostEqual(self.statistics_power["max_distance"], 1259.6, places=1)
        self.assertAlmostEqual(
            self.statistics_heartrate["max_distance_interval"], 13855.4, places=1
        )

    def test_avg_distance_correct(self):
        self.assertAlmostEqual(self.statistics_power["avg_distance"], 479.67, places=2)
        self.assertAlmostEqual(
            self.statistics_heartrate["avg_distance_interval"], 5454.8875, places=4
        )

    def test_min_heartrate_correct(self):
        self.assertAlmostEqual(
            self.statistics_heartrate["min_heartrate_interval"], 167.2958, places=4
        )

    def test_max_heartrate_correct(self):
        self.assertAlmostEqual(
            self.statistics_heartrate["max_heartrate_interval"], 174.23, places=2
        )

    def test_avg_heartrate_correct(self):
        self.assertAlmostEqual(
            self.statistics_heartrate["avg_heartrate_interval"], 170.61, places=2
        )
