import overpy

from sport_activities_features.interruptions.exercise import TrackSegment
from sport_activities_features.interruptions.exercise_event import ExerciseEvent

class CoordinatesBox:
    def __init__(self, min_latitude=300, min_longitude=300, max_latitude=-300, max_longitude=-300,
                 event: ExerciseEvent = ExerciseEvent()):
        self.min_latitude = min_latitude
        self.min_longitude = min_longitude
        self.max_latitude = max_latitude
        self.max_longitude = max_longitude
        if len(event.event) > 0:
            self.define_event_box_size(event)

    def expand(self):
        """
        :return: expands the total area by 0.003 degrees (so that all intersections are included)
        """
        self.min_longitude -= 0.003
        self.min_latitude -= 0.003
        self.max_longitude += 0.003
        self.max_latitude += 0.003

    def define_event_box_size(self, event: ExerciseEvent):
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
        self.expand()


class Overpass:
    def __init__(self, api_url):
        self.api = overpy.Overpass(url=api_url)

    def identify_intersections(self, event, box: CoordinatesBox):
        """
        :param event: Event object with pre, event, post
        :param box: boundaries of intersections on the map
        :return: possible intersections
        """
        query = f'''way 
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
        }}'''
        return self.api.query(query)
