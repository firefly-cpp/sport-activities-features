import os
from unittest import TestCase

from sport_activities_features.dead_end_identification import (
    DeadEndIdentification
)
from sport_activities_features.tcx_manipulation import TCXFile


class TestDeadEndIdentification(TestCase):
    def setUp(self):
        # Reading the TCX file.
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        tcx_file = TCXFile()
        self.activity = tcx_file.read_one_file(filename)

        self.positions = np.array([*activity['positions']])
        self.distances = np.array([*activity['distances']])

    def dead_end_test(self):
        Dead_ends = DeadEndIdentification(positions,
                                  distances,
                                  tolerance_degrees=1,
                                  tolerance_position=2,
                                  minimum_distance=500)
        result = Dead_ends.identify_dead_ends()

        self.assertEqual(result, None)
