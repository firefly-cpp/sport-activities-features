import os
from unittest import TestCase

from sport_activities_features import TCXFile


class TestTCXFile(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        self.tcx_file: TCXFile = TCXFile()
        tcx_exercise = self.tcx_file.read_one_file(filename)
        self.data_with_missing = self.tcx_file.extract_activity_data(tcx_exercise)
        self.data_without_missing = self.tcx_file.extract_activity_data(tcx_exercise)
        self.tcx_file.linear_fill_missing_values(
            self.data_without_missing, 'heartrates', 15,
        )

    def test_missing_values_filled(self):
        after = self.tcx_file.count_missing_values(
            self.data_without_missing['heartrates'],
        )
        before = self.tcx_file.count_missing_values(
            self.data_with_missing['heartrates'],
        )
        assert before == 5
        assert after == 0

    # def test_missing_values_averages(self):
    #    predicted_values = [150, 150, 150, 150, 149]
    #    actual_values = self.data_without_missing['heartrates'][2959:2964]
    #    for i in range(0, 5):
    #        assert predicted_values[i] == actual_values[i]
