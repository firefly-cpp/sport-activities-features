import datetime
import os
from unittest import TestCase

from sport_activities_features.interval_identification import (
    IntervalIdentificationByHeartRate,
    IntervalIdentificationByPower,
)
from sport_activities_features.tcx_manipulation import TCXFile


class TestIntervalIdentificationActivity(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '2.tcx')
        tcx_file = TCXFile()
        tcx_exercise = tcx_file.read_one_file(filename)
        self.activity = tcx_file.extract_activity_data(tcx_exercise)

        # Identifying the intervals in the activity by power
        IntervalsPower = IntervalIdentificationByPower(
            self.activity['distances'],
            self.activity['timestamps'],
            self.activity['altitudes'],
            70,
        )
        IntervalsPower.identify_intervals()
        self.statistics_power = IntervalsPower.calculate_interval_statistics()

        # Identifying the intervals in the activity by heart rate
        IntervalsHeartrate = IntervalIdentificationByHeartRate(
            self.activity['distances'],
            self.activity['timestamps'],
            self.activity['altitudes'],
            self.activity['heartrates'],
        )
        IntervalsHeartrate.identify_intervals()
        self.statistics_heartrate = (
            IntervalsHeartrate.calculate_interval_statistics()
        )

    def test_num_intervals_correct(self):
        self.assertEqual(self.statistics_power['number_of_intervals'], 18)
        self.assertEqual(self.statistics_heartrate['number_of_intervals'], 3)

    def test_min_duration_correct(self):
        self.assertAlmostEqual(
            self.statistics_power['min_duration'], 30.0, places=1)
        self.assertAlmostEqual(
            self.statistics_heartrate['min_duration_interval'], 184.0, places=1
        )

    def test_max_duration_correct(self):
        self.assertAlmostEqual(
            self.statistics_power['max_duration'], 207.0, places=1)
        self.assertAlmostEqual(
            self.statistics_heartrate['max_duration_interval'],
            2191.0,
            places=1
        )

    def test_avg_duration_correct(self):
        self.assertAlmostEqual(
            self.statistics_power['avg_duration'],
            89.28,
            places=2
        )
        self.assertAlmostEqual(
            self.statistics_heartrate['avg_duration_interval'],
            1169.0,
            places=2
        )

    def test_min_distance_correct(self):
        self.assertAlmostEqual(
            self.statistics_power['min_distance'],
            152.8203,
            places=4
        )
        self.assertAlmostEqual(
            self.statistics_heartrate['min_distance_interval'],
            1500.90,
            places=2
        )

    def test_max_distance_correct(self):
        self.assertAlmostEqual(
            self.statistics_power['max_distance'],
            1259.6,
            places=1
        )
        self.assertAlmostEqual(
            self.statistics_heartrate['max_distance_interval'],
            13855.4,
            places=1
        )

    def test_avg_distance_correct(self):
        self.assertAlmostEqual(
            self.statistics_power['avg_distance'],
            509.81,
            places=2
        )
        self.assertAlmostEqual(
            self.statistics_heartrate['avg_distance_interval'],
            7669.2700,
            places=4
        )

    def test_min_heartrate_correct(self):
        self.assertAlmostEqual(
            self.statistics_heartrate['min_heartrate_interval'],
            167.4933,
            places=4
        )

    def test_max_heartrate_correct(self):
        self.assertAlmostEqual(
            self.statistics_heartrate['max_heartrate_interval'],
            171.45,
            places=2
        )

    def test_avg_heartrate_correct(self):
        self.assertAlmostEqual(
            self.statistics_heartrate['avg_heartrate_interval'],
            169.47,
            places=2
        )


START = datetime.datetime(2026, 1, 1, 10, 0, 0)


def seconds(n):
    """Timestamps one second apart."""
    return [START + datetime.timedelta(seconds=i) for i in range(n)]


def heart_rate_intervals(heart_rates, minimum_time=30):
    n = len(heart_rates)
    intervals = IntervalIdentificationByHeartRate(
        list(range(n)), seconds(n), [0] * n, heart_rates,
        minimum_time=minimum_time,
    )
    intervals.identify_intervals()
    return intervals


def power_intervals(speeds, minimum_time=30):
    """Flat ride with the given speed (m/s) for every second."""
    distances = [0]
    for speed in speeds:
        distances.append(distances[-1] + speed)
    n = len(distances)
    intervals = IntervalIdentificationByPower(
        distances, seconds(n), [0] * n, 70, minimum_time=minimum_time,
    )
    intervals.identify_intervals()
    return intervals


def spans(intervals):
    return [(i[0], i[-1]) for i in intervals.return_intervals()]


class TestIntervalIdentificationByHeartRate(TestCase):
    def test_interval_at_the_end_is_kept(self):
        intervals = heart_rate_intervals([100] * 100 + [180] * 100)
        self.assertEqual(spans(intervals), [(100, 199)])

    def test_every_interval_is_long_enough(self):
        # 60 s interval, then a 20 s interval (too short) as the last one
        intervals = heart_rate_intervals(
            [100] * 100 + [180] * 60 + [100] * 100 + [180] * 20 + [100] * 50,
        )
        self.assertEqual(spans(intervals), [(100, 159)])

    def test_last_pair_of_intervals_is_merged(self):
        # Short dip between the last two intervals with a heart rate close
        # to the average: they become one interval.
        intervals = heart_rate_intervals(
            [100] * 100 + [180] * 60 + [100] * 100
            + [180] * 40 + [139] * 5 + [180] * 40,
        )
        self.assertEqual(spans(intervals), [(100, 159), (260, 344)])

    def test_numpy_heart_rates(self):
        import numpy as np
        intervals = heart_rate_intervals(
            list(np.array([100] * 100 + [180] * 100)),
        )
        self.assertEqual(spans(intervals), [(100, 199)])

    def test_short_missing_heart_rate_does_not_split_interval(self):
        intervals = heart_rate_intervals(
            [100] * 100 + [180] * 30 + [None] * 5 + [180] * 30 + [100] * 35,
        )
        self.assertEqual(spans(intervals), [(100, 164)])

    def test_missing_heart_rate_at_the_end(self):
        intervals = heart_rate_intervals([100] * 100 + [180] * 99 + [None])
        self.assertEqual(spans(intervals), [(100, 198)])

    def test_long_missing_heart_rate_raises(self):
        with self.assertRaises(ValueError):
            heart_rate_intervals([100] * 50 + [None] * 20 + [180] * 50)

    def test_statistics(self):
        intervals = heart_rate_intervals(
            [100] * 100 + [180] * 61 + [100] * 100 + [170] * 41,
        )
        statistics = intervals.calculate_interval_statistics()
        self.assertEqual(statistics['number_of_intervals'], 2)
        self.assertEqual(statistics['min_duration_interval'], 40)
        self.assertEqual(statistics['max_duration_interval'], 60)
        self.assertEqual(statistics['avg_distance_interval'], 50)
        self.assertEqual(statistics['min_heartrate_interval'], 170)
        self.assertEqual(statistics['max_heartrate_interval'], 180)

    def test_statistics_without_intervals(self):
        statistics = heart_rate_intervals(
            [150] * 100,
        ).calculate_interval_statistics()
        self.assertEqual(statistics['number_of_intervals'], 0)
        self.assertIsNone(statistics['avg_duration_interval'])
        self.assertIsNone(statistics['avg_heartrate_interval'])


class TestIntervalIdentificationByPower(TestCase):
    def test_interval_at_the_end_is_kept(self):
        intervals = power_intervals([5] * 100 + [12] * 100)
        self.assertEqual(spans(intervals), [(100, 199)])

    def test_every_interval_is_long_enough(self):
        # 60 s interval, then a 10 s interval (too short) as the last one
        intervals = power_intervals(
            [5] * 100 + [12] * 60 + [5] * 100 + [12] * 10 + [5] * 50,
        )
        self.assertEqual(spans(intervals), [(100, 159)])

    def test_close_intervals_are_merged(self):
        # Last two intervals 10 s apart (< 30 s): merged.
        intervals = power_intervals(
            [5] * 100 + [12] * 60 + [5] * 100 + [12] * 40 + [5] * 10
            + [12] * 40,
        )
        self.assertEqual(spans(intervals), [(100, 159), (260, 349)])

    def test_statistics_without_intervals(self):
        statistics = power_intervals(
            [8] * 100,
        ).calculate_interval_statistics()
        self.assertEqual(statistics['number_of_intervals'], 0)
        self.assertIsNone(statistics['min_duration'])
        self.assertIsNone(statistics['avg_distance'])

    def test_missing_altitudes_are_treated_as_flat(self):
        n = 201
        distances = [0]
        for i in range(n - 1):
            distances.append(distances[-1] + (12 if i >= 100 else 5))
        complete = IntervalIdentificationByPower(
            distances, seconds(n), [0] * n, 70,
        )
        complete.identify_intervals()
        missing = IntervalIdentificationByPower(
            distances, seconds(n), [None] * n, 70,
        )
        missing.identify_intervals()
        self.assertEqual(missing.powers, complete.powers)
        self.assertEqual(spans(missing), [(100, 199)])

    def test_missing_distance_gives_zero_power(self):
        n = 201
        distances = [i * 5 for i in range(n)]
        distances[50] = None
        intervals = IntervalIdentificationByPower(
            distances, seconds(n), [0] * n, 70,
        )
        intervals.identify_intervals()
        self.assertEqual(intervals.powers[49], 0)
        self.assertEqual(intervals.powers[50], 0)
        self.assertGreater(intervals.powers[51], 0)
