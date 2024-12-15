import os
from unittest import TestCase

from sport_activities_features import InterruptionProcessor, TCXFile
from sport_activities_features.interruptions.exercise_event import EventType


class TestInterruptionProcessor(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        tcx_file = TCXFile()
        tcx_exercise = tcx_file.read_one_file(filename)
        tcx = tcx_file.extract_activity_data(tcx_exercise)

        interruptionProcessor = InterruptionProcessor(
            time_interval=60,
            min_speed=2,
            overpass_api_url='url_to_overpass_api',
        )
        """
        Set to false because we don't have Overpass API avaliable
        in localhost every time. Only interruptions are tested.
        Intersections are not tested because they depend on an
        external dependency.
        """
        self.data = interruptionProcessor.events(tcx, False)

    def test_number_of_detected_events(self):
        assert len(self.data) == 14

    def test_specific_event(self):
        assert len(self.data[3].pre_event) == 25
        assert len(self.data[3].post_event) == 21

    def test_start_end_event(self):
        assert self.data[0].event_type == EventType.EXERCISE_START
        assert self.data[-1].event_type == EventType.EXERCISE_STOP
