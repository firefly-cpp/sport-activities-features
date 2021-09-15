from unittest import TestCase
from sport_activities_features.classes import StoredSegments


class StoredSegmentsTestCase(TestCase):
    def setUp(self):
        self.__stored_segments = StoredSegments([3.5, 5.55, 3.44], 165.22)

    def test_init_stored_segments_works_fine(self):
        arr = [3.5, 5.55, 3.44]
        self.assertCountEqual(arr, self.__stored_segments.segment)
        self.assertEqual(165.22, self.__stored_segments.ascent)
