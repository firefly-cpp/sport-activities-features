from datetime import datetime
from enum import Enum

from sport_activities_features.interruptions.exercise import TrackSegment


class EventType(Enum):

    """Enum for classifying event type."""

    UNDEFINED = -1
    EXERCISE_START = 0
    EXERCISE_STOP = 1
    EXERCISE_PAUSE = 2


class EventDetailType(Enum):

    """Enum for determining the details of interruption event.
    Currently only Intersections can be identified, but if the algorithm is
    extended in the future also road bends and other types of obstacles will
    be detected.
    """

    UNDEFINED = -1  # WORKS
    INTERSECTION = 0  # WORKS
    ROAD_BEND = 1  # TO-DO
    UNKNOWN_OBSTACLE = 2  # TO-DO


class EventLocation:

    """Class for holding the latitude and longitude of event."""

    def __init__(self, longitude, latitude) -> None:
        self.longitude = longitude
        self.latitude = latitude


class EventDetail:

    """Class for holding the EventLocation and EventDetailType."""

    def __init__(
        self,
        location: EventLocation = None,
        type: EventDetailType = EventDetailType.UNDEFINED,
    ) -> None:
        """Initialisation class for EventDetail.

        Args:
        ----
            location: EventLocation
            type: EventDetailType.
        """
        self.location = location
        self.type = type


class ExerciseEvent:

    """Class for idenitified ExerciseEvents.
    Each event is made from pre event data (recording previous to the event),
    post event data (recording after the event) and actual event (recording
    during which the boundary conditions of event are met).
    """

    def __init__(
        self,
        pre_event: list = [],
        event: list = [],
        post_event: list = [],
        title: str = '',
        event_type: EventType = EventType.UNDEFINED,
        event_detail: EventDetail = EventDetail(),
    ) -> None:
        """Initialisation method for ExerciseEvent class.

        Args:
        ----
            pre_event: [TrackSegment] of before the event
            event: [TrackSegment] of the event
            post_event: [TrackSegment] of after the event
            title: Event title, default value is currently an empty string.
            event_type: Enum EventType
            event_detail: Enum EventDetailType.
        """
        self.pre_event: list = pre_event
        self.event: list = event
        self.post_event: list = post_event
        self.title = title
        self.event_type: EventType = event_type
        self.event_detail: EventDetailType = event_detail

    def add_event(self, segment: TrackSegment):
        """Appends the TrackSegment to the event TrackSegment list.

        Args:
        ----
            segment: TrackSegment of the event.
        """
        self.event.append(segment)

    def add_pre_event(self, segment: TrackSegment):
        """Appends the TrackSegment to the pre event TrackSegment list.

        Args:
        ----
            segment: TrackSegment of the pre event.
        """
        self.pre_event.append(segment)

    def add_post_event(self, segment: TrackSegment):
        """Appends the TrackSegment to the post event TrackSegment list.

        Args:
        ----
            segment: TrackSegment of the post event.
        """
        self.post_event.append(segment)


class EventStats:

    """Class for holding the statistics about the identified event."""

    def __init__(
        self,
        index_start=-1,
        index_mid=-1,
        index_end=-1,
        timestamp_mid_start=None,
        timestamp_mid: datetime = None,
        timestamp_mid_end: datetime = None,
        timestamp_post_end: datetime = None,
        timestamp_pre_start: datetime = None,
    ) -> None:
        """Initialisation method for EventStats object.

        Args:
        ----
            index_start: Start of stoppage
            index_mid: Middle index of stoppage
            index_end: Last index of stoppage
            timestamp_mid_start: imestamp of first index of stoppage
            timestamp_mid: imestamp of middle index of stoppage
            timestamp_mid_end: imestamp of last index of stoppage
            timestamp_post_end: Maximum timestamp of post event observed
            timestamp_pre_start: Earliest timestamp of pre event observed.
        """
        self.index_start = index_start
        self.index_end = index_end
        self.timestamp_mid_start = timestamp_mid_start
        self.timestamp_mid_end = timestamp_mid_end
        self.timestamp_post_end = timestamp_post_end
        self.timestamp_pre_start = timestamp_pre_start
