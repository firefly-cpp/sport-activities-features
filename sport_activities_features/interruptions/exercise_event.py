from datetime import datetime
from enum import Enum

from sport_activities_features.interruptions.exercise import TrackSegment


class EventType(Enum):
    UNDEFINED = -1
    EXERCISE_START = 0
    EXERCISE_STOP = 1
    EXERCISE_PAUSE = 2


class EventDetailType(Enum):
    UNDEFINED = -1  # WORKS
    INTERSECTION = 0  # WORKS
    ROAD_BEND = 1  # TO-DO
    UNKNOWN_OBSTACLE = 2  # TO-DO


class EventLocation:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude


class EventDetail:
    def __init__(self, location: EventLocation = None, type: EventDetailType = EventDetailType.UNDEFINED):
        self.location = location
        self.type = type


class ExerciseEvent:
    def __init__(self, pre_event: [TrackSegment] = [], event: [TrackSegment] = [], post_event: [TrackSegment] = [],
                 title: str = "",
                 event_type: EventType = EventType.UNDEFINED, event_detail: EventDetail = EventDetail()):
        self.pre_event: [TrackSegment] = pre_event
        self.event: [TrackSegment] = event
        self.post_event: [TrackSegment] = post_event
        self.title = title
        self.event_type: EventType = event_type
        self.event_detail = event_detail

    def add_event(self, segment: TrackSegment):
        self.event.append(segment)

    def add_pre_event(self, segment: TrackSegment):
        self.pre_event.append(segment)

    def add_post_event(self, segment: TrackSegment):
        self.post_event.append(segment)


class EventStats:
    def __init__(self, index_start=-1, index_mid=-1, index_end=-1,
                 timestamp_mid_start=None, timestamp_mid: datetime = None, timestamp_mid_end: datetime = None,
                 timestamp_post_end: datetime = None,
                 timestamp_pre_start: datetime = None):
        """
        :param index_start: Start of stoppage
        :param index_mid: Middle index of stoppage
        :param index_end: Last index of stoppage
        :param timestamp_mid_start: imestamp of first index of stoppage
        :param timestamp_mid: imestamp of middle index of stoppage
        :param timestamp_mid_end: imestamp of last index of stoppage
        :param timestamp_post_end: Maximum timestamp of post event observed
        :param timestamp_pre_start: Earliest timestamp of pre event observed
        """
        self.index_start = index_start
        self.index_end = index_end
        self.timestamp_mid_start = timestamp_mid_start
        self.timestamp_mid_end = timestamp_mid_end
        self.timestamp_post_end = timestamp_post_end
        self.timestamp_pre_start = timestamp_pre_start
