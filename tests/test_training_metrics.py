import glob
import os
from datetime import datetime, timedelta
from unittest import TestCase

from tcxreader.tcxreader import TCXExercise, TCXTrackPoint

from sport_activities_features import TCXFile
from sport_activities_features.training_metrics import TrainingMetrics


class TestTrainingMetrics(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '11.tcx')
        self.tcx_file = TCXFile()
        tcx_exercise = self.tcx_file.read_one_file(filename)        
        self.data = self.tcx_file.extract_integral_metrics(tcx_exercise)
        self.raw_data = tcx_exercise
        
    def test_functional_threshold_power(self):
        tm_instance = TrainingMetrics()
        power_data = tm_instance.prepare_functional_threshold_power_data(self.raw_data,30,0)
        ftp = tm_instance.functional_threshold_power(power_data)
        self.assertAlmostEqual(ftp, 72.48, 3)
        
    def test_normalized_power(self):
        tm_instance = TrainingMetrics()
        power_data = tm_instance.prepare_normalized_power_data(self.raw_data,30,0)
        normalized_power = tm_instance.normalized_power(power_data,30)
        self.assertAlmostEqual(normalized_power,75.57,3)
        
    def test_training_stress_score(self):
        tm_instance = TrainingMetrics()
        power_data = tm_instance.prepare_functional_threshold_power_data(self.raw_data,30,0)
        n_power_data = tm_instance.prepare_normalized_power_data(self.raw_data,30,0)
        ftp = tm_instance.functional_threshold_power(power_data)
        normalized_power = tm_instance.normalized_power(n_power_data,30)
        tss = tm_instance.training_stress_score(30,normalized_power,ftp)        
        self.assertAlmostEqual(tss, 0.91, 3)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
START = datetime(2026, 1, 1, 10, 0, 0)


def exercise(watts):
    """Exercise with one trackpoint per second and the given power values
    (None: power missing, ...: no Watts key at all)."""
    trackpoints = []
    for second, value in enumerate(watts):
        extensions = {} if value is ... else {'Watts': value}
        trackpoints.append(TCXTrackPoint(
            time=START + timedelta(seconds=second), tpx_ext=extensions,
        ))
    return TCXExercise(trackpoints=trackpoints)


class TestTrainingMetricsWithoutPower(TestCase):
    def test_sample_files_without_power(self):
        tm = TrainingMetrics()
        tcx_file = TCXFile()
        checked = 0
        for path in sorted(glob.glob(os.path.join(DATA_DIR, '*.tcx'))):
            tcx = tcx_file.read_one_file(path)
            has_power = any(
                (tp.tpx_ext or {}).get('Watts') for tp in tcx.trackpoints
            )
            if has_power:
                continue
            with self.subTest(os.path.basename(path)):
                self.assertEqual(
                    tm.prepare_functional_threshold_power_data(tcx, 1200), 0,
                )
                power_data = tm.prepare_normalized_power_data(tcx, 1200)
                self.assertEqual(power_data, [])
                self.assertIsNone(tm.normalized_power(power_data, 30))
            checked += 1
        self.assertGreaterEqual(checked, 5)


class TestTrainingMetricsWindow(TestCase):
    def setUp(self):
        self.tm = TrainingMetrics()

    def test_window_and_offset(self):
        tcx = exercise(list(range(1, 101)))  # 1 W, 2 W, ... 100 W
        self.assertEqual(
            self.tm.prepare_normalized_power_data(tcx, 4, 10),
            [11, 12, 13, 14, 15],
        )
        self.assertEqual(
            self.tm.prepare_functional_threshold_power_data(tcx, 4, 10), 13,
        )

    def test_float_window_and_offset(self):
        tcx = exercise(list(range(1, 101)))
        self.assertEqual(
            self.tm.prepare_normalized_power_data(tcx, 4.5, 10.5),
            [12, 13, 14, 15, 16],
        )
        self.assertEqual(
            self.tm.prepare_functional_threshold_power_data(tcx, 1200.0),
            50.5,
        )

    def test_missing_power_holds_and_zero_power_is_kept(self):
        # The window starts at the first power above 0 W (third second).
        # Seconds without a power value keep the last value (200 W);
        # zero power (coasting) is part of the data.
        tcx = exercise([None, ..., 0, 200, None, ..., 0, 300])
        self.assertEqual(
            self.tm.prepare_normalized_power_data(tcx, 60),
            [200, 200, 200, 0, 300],
        )

    def test_default_ftp_window_is_20_minutes(self):
        tcx = exercise([100] * 1200 + [400] * 600)
        self.assertEqual(
            self.tm.prepare_functional_threshold_power_data(tcx),
            (1200 * 100 + 400) / 1201,  # 0 s to 1200 s inclusive
        )

    def test_float_window_on_activity(self):
        tcx = TCXFile().read_one_file(os.path.join(DATA_DIR, '11.tcx'))
        self.assertEqual(
            self.tm.prepare_functional_threshold_power_data(tcx, 1200.0),
            self.tm.prepare_functional_threshold_power_data(tcx, 1200),
        )


class TestTrainingMetricsFormulas(TestCase):
    def setUp(self):
        self.tm = TrainingMetrics()

    def test_normalized_power_of_constant_power(self):
        self.assertEqual(self.tm.normalized_power([250] * 60, 30), 250)

    def test_normalized_power(self):
        power = [100] * 30 + [300] * 30
        rolling = [
            sum(power[i:i + 30]) / 30 for i in range(len(power) - 29)
        ]
        expected = (sum(r ** 4 for r in rolling) / len(rolling)) ** 0.25
        self.assertAlmostEqual(
            self.tm.normalized_power(power, 30), round(expected, 2),
        )

    def test_normalized_power_without_enough_data(self):
        self.assertIsNone(self.tm.normalized_power([], 30))
        self.assertIsNone(self.tm.normalized_power([200] * 29, 30))

    def test_training_stress_score_of_one_hour_at_ftp(self):
        self.assertEqual(self.tm.training_stress_score(3600, 250, 250), 100)

    def test_invalid_ftp(self):
        for ftp in (0, -10, None):
            with self.assertRaises(ValueError):
                self.tm.calculate_intensity_factor(200, ftp)
            with self.assertRaises(ValueError):
                self.tm.training_stress_score(3600, 200, ftp)


def exercise_at(samples):
    """Exercise from (second, watts) samples."""
    return TCXExercise(trackpoints=[
        TCXTrackPoint(
            time=START + timedelta(seconds=second), tpx_ext={'Watts': watts},
        )
        for second, watts in samples
    ])


class TestBestAveragePower(TestCase):
    def setUp(self):
        self.tm = TrainingMetrics()

    def test_activity(self):
        tcx = TCXFile().read_one_file(os.path.join(DATA_DIR, '11.tcx'))
        # 11.tcx is recorded every second without gaps, so the best
        # 20 minutes is the best average of 1200 consecutive samples.
        watts = [tp.tpx_ext['Watts'] for tp in tcx.trackpoints]
        expected = max(
            sum(watts[i:i + 1200]) / 1200 for i in range(len(watts) - 1199)
        )
        best = self.tm.best_average_power(tcx)
        self.assertAlmostEqual(best, expected, places=2)
        self.assertAlmostEqual(best, 332.57, places=2)
        self.assertAlmostEqual(
            self.tm.estimate_functional_threshold_power(tcx),
            round(0.95 * best, 2),
        )
        # Power curve: shorter efforts are at least as hard.
        self.assertGreaterEqual(
            self.tm.best_average_power(tcx, 60),
            self.tm.best_average_power(tcx, 300),
        )
        self.assertGreaterEqual(self.tm.best_average_power(tcx, 300), best)

    def test_best_block(self):
        # 30 min at 200 W with 5 min at 300 W in the middle
        tcx = exercise([200] * 900 + [300] * 300 + [200] * 600)
        self.assertEqual(self.tm.best_average_power(tcx), 225)
        self.assertEqual(self.tm.best_average_power(tcx, 300), 300)
        self.assertEqual(self.tm.estimate_functional_threshold_power(tcx), 213.75)

    def test_zero_power_counts(self):
        tcx = exercise([0, 400] * 900)
        self.assertEqual(self.tm.best_average_power(tcx), 200)

    def test_irregular_sampling(self):
        # One sample every 5 s gives the same result as every second.
        every_second = exercise([250] * 1500)
        every_5_seconds = exercise_at([(s, 250) for s in range(0, 1500, 5)])
        self.assertEqual(self.tm.best_average_power(every_second), 250)
        self.assertEqual(self.tm.best_average_power(every_5_seconds), 250)

    def test_long_gap_counts_as_zero(self):
        # 10 min at 300 W (samples at 0-599 s), no samples until 660 s
        # (auto-pause), 10 min at 300 W (660-1259 s). The sample at 599 s
        # covers 10 s (599-608 s), the remaining 51 s count as 0 W, so
        # 1209 of the 1260 seconds are at 300 W. The best 20 minutes
        # leaves out 60 s at 300 W: (1209 - 60) * 300 / 1200 = 287.25.
        samples = [(s, 300) for s in range(600)]
        samples += [(s, 300) for s in range(660, 1260)]
        tcx = exercise_at(samples)
        self.assertEqual(self.tm.best_average_power(tcx), 287.25)

    def test_not_enough_data(self):
        self.assertIsNone(self.tm.best_average_power(exercise([300] * 1199)))
        self.assertIsNone(
            self.tm.estimate_functional_threshold_power(exercise([300] * 600)),
        )
        tcx = TCXFile().read_one_file(os.path.join(DATA_DIR, '15.tcx'))
        self.assertIsNone(self.tm.best_average_power(tcx))
        self.assertIsNone(self.tm.estimate_functional_threshold_power(tcx))


def reference_normalized_power(watts_per_second):
    """Normalized power straight from the definition."""
    rolling = [
        sum(watts_per_second[i:i + 30]) / 30
        for i in range(len(watts_per_second) - 29)
    ]
    return (sum(r ** 4 for r in rolling) / len(rolling)) ** 0.25


class TestNormalizedPowerOfActivity(TestCase):
    def setUp(self):
        self.tm = TrainingMetrics()

    def test_activity(self):
        tcx = TCXFile().read_one_file(os.path.join(DATA_DIR, '11.tcx'))
        watts = [tp.tpx_ext['Watts'] for tp in tcx.trackpoints]
        first = next(i for i, w in enumerate(watts) if w > 0)
        # 11.tcx is recorded every second without gaps.
        expected = reference_normalized_power(watts[first:])

        power_data = self.tm.prepare_normalized_power_data(tcx)
        self.assertEqual(len(power_data), len(watts) - first)
        np_value = self.tm.normalized_power_of_activity(tcx)
        self.assertAlmostEqual(np_value, round(expected, 2), places=2)
        self.assertEqual(np_value, self.tm.normalized_power(power_data))
        # NP is never below the average power.
        self.assertGreaterEqual(np_value, sum(watts[first:]) / len(watts[first:]))

    def test_window_is_in_seconds_not_samples(self):
        # The same ride recorded every second and every 2 seconds:
        # 1 min at 100 W / 1 min at 300 W, five times.
        profile = ([100] * 60 + [300] * 60) * 5
        every_second = exercise(profile)
        every_2_seconds = exercise_at(
            [(s, w) for s, w in enumerate(profile) if s % 2 == 0],
        )
        expected = round(reference_normalized_power(profile), 2)
        self.assertEqual(
            self.tm.normalized_power_of_activity(every_second), expected,
        )
        self.assertEqual(
            self.tm.normalized_power_of_activity(every_2_seconds), expected,
        )

    def test_constant_power(self):
        self.assertEqual(
            self.tm.normalized_power_of_activity(exercise([220] * 600)), 220,
        )

    def test_not_enough_data(self):
        self.assertIsNone(
            self.tm.normalized_power_of_activity(exercise([220] * 29)),
        )
        tcx = TCXFile().read_one_file(os.path.join(DATA_DIR, '15.tcx'))
        self.assertIsNone(self.tm.normalized_power_of_activity(tcx))

    def test_training_stress_score_of_activity(self):
        tcx = exercise([250] * 3600)
        ftp = 250
        np_value = self.tm.normalized_power_of_activity(tcx)
        self.assertEqual(self.tm.training_stress_score(3600, np_value, ftp), 100)
