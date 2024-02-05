from datetime import timedelta, datetime
from typing import TYPE_CHECKING

from geopy import distance

from sport_activities_features.interruptions.exercise import TrackSegment
from sport_activities_features.interruptions.exercise_event import (
    EventDetail,
    EventDetailType,
    EventLocation,
    EventStats,
    EventType,
    ExerciseEvent,
)
from sport_activities_features.interruptions.overpass import (
    CoordinatesBox,
    Overpass,
)

if TYPE_CHECKING:
    import overpy

class IntersectionHelperPoint:
    latitude: float
    longitude: float
    time: datetime
    elevation: float = None
    heartrate: int = None
    distance: float = None
    speed: float = None

    def __repr__(self):
        return f"<IntersectionHelperPoint lat={self.latitude} lon={self.longitude} time={self.time}>"


class InterruptionProcessor():

    """Class for identifying interruption events (events
    where the speed dropped below threshold).

    Args:
    ----
        time_interval: Record x seconds before and after the event
        min_speed: Speed threshold for the event to trigger
                   (min_speed = 2 -> trigger if speed less than 2km/h)
        overpass_api_url: Overpass API url. Self-hosting is prefferable
                          if you want to make a lot of requests.
    """

    def __init__(
        self,
        time_interval=60,
        min_speed=2,
        overpass_api_url='https://lz4.overpass-api.de/api/interpreter',
    ) -> None:
        """Initialisation method of InterruptionProcessor class.

        Args:
        ----
            time_interval: Record x seconds before and after the event
            min_speed: Speed threshold for the event to trigger
                       (min_speed = 2 -> trigger if speed less than 2km/h)
            overpass_api_url: Overpass API url, self host if you want
                              to make a lot of requests.
        """
        self.time_interval = time_interval
        self.min_speed = min_speed
        self.overpass_api_url = overpass_api_url

    def __determine_event_type(
        self,
        event_stats: EventStats,
        lines: list,
    ):
        """Method that idenitifies type of interruption event based on
        position of the event in regards to the complete training.

        Args:
        ----
            event_stats: EventStats of the identified event
            lines: [TrackSegment] of the event
        Returns:
            Returns Enum EventType if this ia a event of type
            exercise start, exercise end or actual interruption.
        """
        if event_stats.index_start == 0:
            return EventType.EXERCISE_START
        elif event_stats.index_end >= len(lines) - 1:
            return EventType.EXERCISE_STOP
        else:
            return EventType.EXERCISE_PAUSE

    def __data_to_lines(self, tcx_data) -> list:
        """Method for transforming TCXFile/GPXFile data into [TrackSegment] list.

        Args:
        ----
            tcx_data: TCXData/GPXData generated dictionary
        Returns: list of TrackSegments.
        """
        lines: list = []
        for i in range(len(tcx_data['positions'])):
            if (i != 0):
                point_a = IntersectionHelperPoint()
                point_b = IntersectionHelperPoint()
                point_a.latitude = tcx_data['positions'][i - 1][0]
                point_a.longitude = tcx_data['positions'][i - 1][1]
                point_a.time = tcx_data['timestamps'][i - 1]

                point_b.latitude = tcx_data['positions'][i][0]
                point_b.longitude = tcx_data['positions'][i][1]
                point_b.time = tcx_data['timestamps'][i]

                if len(tcx_data['altitudes']) == len(tcx_data['positions']):
                    point_a.elevation = tcx_data['altitudes'][i - 1]
                    point_b.elevation = tcx_data['altitudes'][i]

                if len(tcx_data['heartrates']) == len(tcx_data['positions']):
                    point_a.heartrate = tcx_data['heartrates'][i - 1]
                    point_b.heartrate = tcx_data['heartrates'][i]

                if len(tcx_data['distances']) == len(tcx_data['positions']):
                    point_a.distance = tcx_data['distances'][i - 1]
                    point_b.distance = tcx_data['distances'][i]

                if len(tcx_data['speeds']) == len(tcx_data['positions']):
                    point_a.distance = tcx_data['speeds'][i - 1]
                    point_b.distance = tcx_data['speeds'][i]

                prev_speed = None
                if (i > 1):
                    prev_speed = lines[-1].speed
                ts = TrackSegment(point_a, point_b, prev_speed)
                lines.append(ts)

        return lines

    def events(
        self,
        lines: list,
        classify=False,
    ) -> list:
        """Method that parses events (method parse_events()) and
        classifies them (classify_events()) if required.

        Args:
        ----
            lines: [TrackSegment] from TCX/GPX data
            classify: If set to true calls classify_events() method.

        Returns: list of [ExerciseEvent], meaning
                 parsed (and classified) events.
        """
        events = self.parse_events(lines)
        if classify is True:
            classified_events = []
            for e in events:
                classified_events.append(self.classify_event(e))
            return classified_events
        return events

    def parse_events(self, lines: list) -> list:
        """Parses all events (based on the min_speed parameter in the
        class initialisation) and returns ExerciseEvent list.

        Args:
        ----
            lines: list of TrackSegment objects.

        Returns: list of identified ExerciseEvent objects
        """
        if type(lines) is dict:
            lines = self.__data_to_lines(lines)
        eventList: list = []
        index = 0
        while index < len(lines):
            event_stats = EventStats()
            if lines[index].speed.km < self.min_speed:
                # add event
                event = ExerciseEvent([], [], [], '', EventType.UNDEFINED)
                event_stats.index_start = index
                event_stats.timestamp_mid_start = lines[index].point_a.time
                while (index < len(lines) and
                       lines[index].speed.km < self.min_speed):
                    event.add_event(lines[index])
                    event_stats.timestamp_mid_end = lines[index].point_b.time
                    index += 1
                event_stats.index_end = index - 1
                event_stats.timestamp_mid = (
                    event_stats.timestamp_mid_start
                    + (event_stats.timestamp_mid_end
                       - event_stats.timestamp_mid_start)
                    / 2)
                event.event_type = self.__determine_event_type(
                    event_stats,
                    lines,
                )
                event_stats.timestamp_post_end = (
                    event_stats.timestamp_mid_end
                    + timedelta(seconds=(self.time_interval + 1)))
                event_stats.timestamp_pre_start = (
                    event_stats.timestamp_mid_start
                    - timedelta(seconds=self.time_interval))
                # add post event
                indexPost = index
                while (indexPost < len(lines) and
                       (lines[indexPost].point_a.time
                        < event_stats.timestamp_post_end)):
                    event.add_post_event(lines[indexPost])
                    indexPost += 1
                indexStartPre = 0
                while (lines[indexStartPre].point_a.time
                       < event_stats.timestamp_pre_start):
                    indexStartPre += 1
                # add pre event
                while (indexStartPre < len(lines)
                       and (lines[indexStartPre].point_a.time
                            <= event_stats.timestamp_mid_start)):
                    event.add_pre_event(lines[indexStartPre])
                    indexStartPre += 1
                eventList.append(event)
            index += 1
        return eventList

    def classify_event(self, event: ExerciseEvent):
        """Method that classifies the sent ExerciseEvent.
        Currently only identifies events which happened
        in the vicincy of intersections.

        Args:
        ----
            event: ExerciseEvent to be inspected
        Returns: ExerciseEvent on which classification has been performed.
        """
        op = Overpass(self.overpass_api_url)
        event: ExerciseEvent
        box = CoordinatesBox(event=event)
        possible_intersections: overpy.Result = op.identify_intersections(box)
        (events, intersections) = (len(event.event),
                                   len(possible_intersections.nodes))
        min_distance = 1000000
        for e in range(0, events):

            for i in range(0, intersections):
                event_location = (event.event[e].point_a.latitude,
                                  event.event[e].point_a.longitude)
                intersection_location = (
                    float(possible_intersections.nodes[i].lat),
                    float(possible_intersections.nodes[i].lon),
                )
                calculated_distance = distance.distance(
                    event_location,
                    intersection_location,
                ).meters
                if (calculated_distance < 22
                        and calculated_distance < min_distance):
                    min_distance = calculated_distance
                    event.event_detail = EventDetail(
                        EventLocation(
                            longitude=possible_intersections.nodes[i].lat,
                            latitude=possible_intersections.nodes[i].lon,
                        ),
                        type=EventDetailType.INTERSECTION,
                    )
        return event
