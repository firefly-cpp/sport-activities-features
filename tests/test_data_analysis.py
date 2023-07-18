import contextlib
import os
from unittest import TestCase

with contextlib.suppress(BaseException):
    from sport_activities_features.data_analysis import DataAnalysis



class TestDataAnalysis(TestCase):
    def setUp(self):
        self.__data_analysis = DataAnalysis()

    def test_run_analysis(self):
        pipeline = self.__data_analysis.analyze_data(
            os.path.join(os.path.dirname(__file__), 'data', 'test_data.csv'),
            'Accuracy',
            5,
            50,
            'DifferentialEvolution',
            ['AdaBoost', 'Bagging', 'MultiLayerPerceptron'],
            ['SelectKBest', 'SelectPercentile', 'ParticleSwarmOptimization'],
            ['Normalizer', 'StandardScaler'],
        )
        assert str(type(pipeline)) == "<class 'niaaml.pipeline.Pipeline'>"

    def test_load_pipeline(self):
        pipeline = self.__data_analysis.load_pipeline(
            os.path.join(os.path.dirname(__file__), 'data', 'test.ppln'),
        )
        assert str(type(pipeline)) == "<class 'niaaml.pipeline.Pipeline'>"
