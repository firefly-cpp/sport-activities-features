import os
from unittest import TestCase

from tcxreader.tcxreader import TCXReader
from sport_activities_features import TCXFile
from sport_activities_features.training_metrics import TrainingMetrics


class TestTrainingMetrics(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '11.tcx')
        self.tcx_file = TCXFile()
        self.data = self.tcx_file.extract_integral_metrics(filename)
        self.raw_data = TCXReader().read(filename)
        
    def test_functional_threshold_power(self):
        tm_instance = TrainingMetrics()
        ftp = tm_instance.functional_threshold_power(self.data['watts_avg'],70)
        self.assertAlmostEqual(ftp, 204.3, 3)
        
    def test_normalized_power(self):
        tm_instance = TrainingMetrics()
        normalized_power = tm_instance.normalized_power(self.raw_data,30)
        self.assertGreater(0,normalized_power)
        
    def test_training_score_stress(self):
        tm_instance = TrainingMetrics()
        ftp = tm_instance.functional_threshold_power(self.data['watts_avg'],70)
        normalized_power = tm_instance.normalized_power(self.raw_data,30)
        tss = tm_instance.training_score_stress(30,normalized_power,ftp)
        self.assertAlmostEqual(tss, 558.1, 3)