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

    def test_missing_and_zero_power_are_skipped(self):
        tcx = exercise([None, ..., 0, 200, None, ..., 0, 300])
        self.assertEqual(
            self.tm.prepare_normalized_power_data(tcx, 60), [200, 300],
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
