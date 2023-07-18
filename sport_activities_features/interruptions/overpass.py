from typing import TYPE_CHECKING

import overpy

from sport_activities_features.interruptions.exercise_event import (
    ExerciseEvent,
)

if TYPE_CHECKING:
    from sport_activities_features.interruptions.exercise import TrackSegment


class CoordinatesBox:

    """Class for generating a bounding box from which
    the Overpass intersections will be queried.
    """

    def __init__(
        self,
        min_latitude: float = 300,
        min_longitude: float = 300,
        max_latitude: float = -300,
        max_longitude: float = -300,
        event: ExerciseEvent = ExerciseEvent(),
    ) -> None:
        """Initialisation method of CoordinatesBox. If optional parameter
        event is recieved the box is generated from the location of the event.
        Otherwise min_latitude, min_longitude, max_latitude, max_longitude
        can be defined in the initialisation.

        Args:
        ----
            min_latitude: minimum latitude of the event box
            min_longitude: minimum longitude of the event box
            max_latitude: maxiumum latitude of the event box
            max_longitude: minimum longitude of the event box
            event: ExerciseEvent, if full the previous
                   parameters are disregarded.
        """
        self.min_latitude = min_latitude
        self.min_longitude = min_longitude
        self.max_latitude = max_latitude
        self.max_longitude = max_longitude
        if len(event.event) > 0:
            self.define_event_box_size(event)

    def __expand(self):
        """Expands the box by 0.003 degrees longitude and latitude."""
        self.min_longitude -= 0.003
        self.min_latitude -= 0.003
        self.max_longitude += 0.003
        self.max_latitude += 0.003

    def define_event_box_size(self, event: ExerciseEvent):
        """Method for defining the box if the event
        is present in initialisation parameters.

        Args:
        ----
            event: ExerciseEvent from which the latitude and longitude is taken.
        """
        x = CoordinatesBox()
        merged_points = event.pre_event + event.event + event.post_event
        point: TrackSegment
        for point in merged_points:
            if point.point_a.latitude < self.min_latitude:
                self.min_latitude = point.point_a.latitude
            if point.point_a.longitude < x.min_longitude:
                self.min_longitude = point.point_a.longitude
            if point.point_a.latitude > x.max_latitude:
                self.max_latitude = point.point_a.latitude
            if point.point_a.longitude > x.max_longitude:
                self.max_longitude = point.point_a.longitude
        self.__expand()


class Overpass:

    """Class for handling the Overpass API requests.
    Currently used for detecting intersections.

    Args:
    ----
    api_url: str location of the Overpass API
    (default: https://lz4.overpass-api.de/api/interpreter).
    """

    def __init__(self, api_url='https://lz4.overpass-api.de/api/interpreter') -> None:
        """Initialisation method of Overpass handling class.

        Args:
        ----
            api_url: str location of the Overpass API
                     (default: https://lz4.overpass-api.de/api/interpreter).
                     Should be self hosted if a lot of requests are to be made.
        """
        self.api = overpy.Overpass(url=api_url)

    def identify_intersections(self, box: CoordinatesBox):
        """Method for generating a Overpass Query Language query for
        identifying intersections inside the bounding box parameters.

        Args:
        ----
            box: object that defines the minimum
                 and maximum latitude, longitude.
        Returns: List of possible intersections inside the
                 queried box latitude and longitude parameters.
        """
        query = f"""way
          ["highway"]
          ["highway"!~"footway|cycleway|path|service|track"]
          ({box.min_latitude},{box.min_longitude},{box.max_latitude},{box.max_longitude})
          ->.hw;
        foreach.hw->.w{{
          node(w.w)->.ns;
          way(bn.ns)->.w2;
          way.w2
            ["highway"]
            ["highway"!~"footway|cycleway|path|service|track"]
            ->.w2;
          (
            .w2->.w2;
            -
            .w->.w;
        )->.wd;
          node(w.wd)->.n2;
          node(w.w)->.n3;
          node.n2.n3;
          out;
        }}"""
        return self.api.query(query)
