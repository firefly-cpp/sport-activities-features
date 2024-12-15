import os
from unittest import TestCase

from tcxreader.tcxreader import TCXReader
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