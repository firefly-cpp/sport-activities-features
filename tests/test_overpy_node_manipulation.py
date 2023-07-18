import os
import pickle
from unittest import TestCase

from sport_activities_features.overpy_node_manipulation import (
    OverpyNodesReader,
)


class TestWeather(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            'data',
            'nodes_test.temp',
        )
        nodes = None
        with open(filename, 'rb') as input:
            nodes = pickle.load(input)
        # Extract basic data from nodes (you can later on use Hill
        # Identification and Hill Data Extraction on them, it must
        # also be noted that API must be ONLINE)
        overpy_reader = OverpyNodesReader(
            open_elevation_api='https://api.open-elevation.com/api/v1/lookup?',
        )
        self.data = overpy_reader.read_nodes(nodes)

    def test_generated_object_properties(self):
        assert len(list(self.data.keys())) == 5
        assert self.data['positions'] is not None
        assert self.data['altitudes'] is not None
        assert self.data['distances'] is not None

    def test_generated_object_altitudes(self):
        assert self.data['altitudes'][33] == 84
        assert self.data['altitudes'][45] == 100
        assert self.data['altitudes'][28] == 92
