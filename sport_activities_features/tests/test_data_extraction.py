import os
from unittest import TestCase
from sport_activities_features import DataExtractionFromCSV


class TestDataExtraction(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "test_data.csv")
        data_extraction_from_csv = DataExtractionFromCSV()
        self.activities = data_extraction_from_csv.from_file(filename)
        self.rand_activities = data_extraction_from_csv.select_random_activities(4)

    def test_number_of_activities_correct(self):
        self.assertEqual(len(self.activities), 306)

    def test_number_of_features_correct(self):
        self.assertEqual(self.activities.shape[1], 9)

    def test_instance_correct(self):
        self.assertEqual(self.activities.iloc[0].duration, 8424.0)

    def test_random_activities_correct(self):
        self.assertEqual(len(self.rand_activities), 4)
