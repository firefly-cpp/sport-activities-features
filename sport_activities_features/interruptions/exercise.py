from math import sqrt

from geopy import distance

from sport_activities_features.gpx_manipulation import GPXTrackPoint
from sport_activities_features.tcx_manipulation import TCXTrackPoint


class Speed:

    """Class for saving the speed in km/h and m/s."""

    def __init__(self, km: float, m: float) -> None:
        """Initialisation method for Speed class
        Args:
            km: speed in km/h
            m : speed in m/s.
        """
        self.km = km
        self.m = m


class TrackSegment:

    """Class for saving pairs of points (point_a, point_b)
    to aid in interruption detection.

    Args:
    ----
        point_a (): GPXTrackPoint or TCXTrackPoint of the start of the line
        point_b (): GPXTrackPoint or TCXTrackPoint of the end of the line
        previous_speed (): Speed at previous TrackSegment
    """

    def __init__(self, point_a, point_b, previous_speed=None) -> None:
        """Initialisation method for TrackSegment class.

        Args:
        ----
            point_a (): GPXTrackPoint or TCXTrackPoint of the start of the line
            point_b (): GPXTrackPoint or TCXTrackPoint of the end of the line
            previous_speed (): Speed at previous TrackSegment.
        """
        self.point_a = point_a
        self.point_b = point_b
        self.__distance()
        self.__time_between_points()
        self.__speed()
        self.__acceleration(previous_speed)
        if (type(self.point_a) is GPXTrackPoint and
                type(self.point_b) is GPXTrackPoint):
            (self.point_a.extensions, self.point_b.extensions) = (None, None)
            (self.point_a.gpx_10_fields, self.point_b.gpx_10_fields) = \
                (None, None)
            (self.point_a.gpx_11_fields, self.point_b.gpx_11_fields) = \
                (None, None)

    def __distance(self):
        if (type(self.point_a) is GPXTrackPoint and
                type(self.point_b) is GPXTrackPoint):
            location_a = (self.point_a.latitude, self.point_a.longitude)
            location_b = (self.point_a.latitude, self.point_b.longitude)
        elif (type(self.point_a) is TCXTrackPoint and
              type(self.point_b) is TCXTrackPoint):
            location_a = (self.point_a.latitude, self.point_a.longitude)
            location_b = (self.point_b.latitude, self.point_b.longitude)
        else:
            location_a = (self.point_a.latitude, self.point_a.longitude)
            location_b = (self.point_b.latitude, self.point_b.longitude)

        flat_distance = distance.distance(location_a, location_b).meters
        if (self.point_a.elevation is not None and
                self.point_b.elevation is not None):
            self.distance = sqrt(
                flat_distance ** 2 +
                (self.point_a.elevation * 0.001 -
                 self.point_b.elevation * 0.001) ** 2)
        else:
            self.distance = flat_distance

    def __time_between_points(self):
        """Method for calculating timedelta between two points."""
        self.difference = self.point_b.time - self.point_a.time

    def __speed(self):
        """Method for calculating speed from two points
        distances and delta time between them.
        """
        seconds = self.difference.seconds if self.difference.seconds > 0 else 1
        self.speed = Speed(
            km=(self.distance / seconds) * 3.6,
            m=(self.distance / seconds),
        )

    def __acceleration(self, previous_speed):
        """Method for calculating acceleration in m/s from previous
        TrackSegment speed and this TrackSegment speed and delta
        time between them.

        Args:
        ----
            previous_speed (): speed in previous TrackSegment.

        Returns:
        -------

        """
        if previous_speed is not None:
            if self.difference.total_seconds() == 0:
                self.acceleration = 0
            else:
                self.acceleration = ((self.speed.m - previous_speed.m) /
                                     self.difference.total_seconds())
        else:
            self.acceleration = 0
