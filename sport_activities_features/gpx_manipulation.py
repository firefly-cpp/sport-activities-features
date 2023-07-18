import os
from typing import TYPE_CHECKING

import geopy
import gpxpy
import numpy as np

from sport_activities_features.file_manipulation import FileManipulation

if TYPE_CHECKING:
    from tcxreader.tcxreader import TCXTrackPoint


class GPXTrackPoint:

    """Class for saving GPX point records.\n
    Args:
        longitude (float):
            longitude in degrees
        latitude (float):
            latitude in degrees
        elevation (float):
            elevation in meters
        time (datetime):
            datetime of time at the given point
        distance (float):
            total distance travelled until this point
        hr_value (int):
            heart beats per minute at given recording.
        cadence (int):
            cadence
        watts (float):
            watts power rating
        speed (float):
            speed in km/h.
    """

    def __init__(
        self,
        longitude: float = None,
        latitude: float = None,
        elevation: float = None,
        time=None,
        distance=None,
        hr_value: int = None,
        cadence=None,
        watts: float = None,
        speed: float = None,
    ) -> None:
        """Initialisation method for GPXTrackPoint class.\n
        Args:
            longitude (float):
                longitude in degrees
            latitude (float):
                latitude in degrees
            elevation (float):
                elevation in meters
            time (datetime):
                datetime of time at the given point
            distance (float):
                total distance travelled until this point
            hr_value (int):
                heart beats per minute at given recording.
            cadence (int):
                cadence
            watts (float):
                watts power rating
            speed (float):
                speed in km/h.
        """
        self.elevation = elevation
        self.latitude = latitude
        self.longitude = longitude
        self.time = time
        self.speed = speed
        self.distance = distance
        self.hr_value = hr_value
        self.cadence = cadence
        self.watts = watts

    def from_GPX(
        self,
        gpx: gpxpy.gpx.GPXTrackPoint,
        hr_value: int = None,
        cadence: int = None,
        watts: int = None,
    ) -> None:
        """Helper method for initialising GPXTrackPoint
        from the gpxpy.gpx.GpxTrackPoint.\n
        Args:
            gpx (gpxpy.gpx.GPXTrackPoint):
                gpxpy.gpx.GPXTrackPoint not to be confused
                with class of the same name used in
                gpx_manipulation
            hr_value (int):
                heart beats per minute at given recording
            cadence (int):
                cadence
            watts (int):
                watts power rating.
        """
        self.elevation = gpx.elevation
        self.latitude = gpx.latitude
        self.longitude = gpx.longitude
        self.time = gpx.time
        self.hr_value = hr_value
        self.cadence = cadence
        self.watts = watts


class GPXFile(FileManipulation):

    """Class for reading GPX files."""

    def __init__(self) -> None:
        """Initialisation method for GPXFile class."""
        self.all_files = []

    def __ascent(self, altitudes: list) -> int:
        """Method for calculating the total ascent from a list of altitudes.\n
        Args:
            altitudes (list):
                list of altitudes from the recorded training
        Returns:
            int: total ascent in meters.
        """
        ascent = 0
        for index, altitude in enumerate(altitudes):
            if index != 0 and altitudes[index - 1] < altitude:
                ascent += altitude - altitudes[index - 1]
        return ascent

    def __descent(self, altitudes: list) -> int:
        """Method for calculating the total descent from a list of altitudes.\n
        Args:
            altitudes (list):
                list of altitudes from the recorded training
        Returns:
            int: total descent in meters.
        """
        descent = 0
        for index, altitude in enumerate(altitudes):
            if index != 0 and altitudes[index - 1] > altitude:
                descent += altitudes[index - 1] - altitude
        return descent

    def read_directory(self, directory_name: str) -> list:
        """Method for finding all GPX files in a directory.\n
        Args:
            directory_name (str):
                name of the directory in which to identify GPX files
        Returns:
            list: array of paths to the identified files.
        """
        files = os.listdir(directory_name)
        all_files1 = [i for i in files if i.endswith('.gpx')]
        for j in range(len(all_files1)):
            file = os.path.join(directory_name, all_files1[j])
            self.all_files.append(file)
        return self.all_files

    def read_one_file(self, filename, numpy_array=False):
        """Method for parsing one GPX file.\n
        Args:
            filename (str):
                name of the TCX file to be read
            numpy_array (bool):
                if set to true dictionary lists are
                transformed into numpy.arrays
        Returns: activity: {
                    'activity_type': activity_type,
                    'positions': positions,
                    'altitudes': altitudes,
                    'distances': distances,
                    'total_distance': total_distance,
                    'timestamps': timestamps,
                    'heartrates': heartrates,
                    'speeds': speeds
                 }.

        Note:
        ----
            In the case of missing value in raw data, we assign None.
        """
        NAMESPACE = '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}'
        points = []
        gpx = None
        try:
            gpx_file = open(filename, encoding='utf-8')
            gpx = gpxpy.parse(gpx_file)
        except Exception:
            gpx_file = open(filename)
            gpx = gpxpy.parse(gpx_file)
        previous_point = None
        for track in gpx.tracks:
            for segment in track.segments:
                for point_gpx in segment.points:
                    trackpoint = GPXTrackPoint()
                    trackpoint.from_GPX(point_gpx)
                    if len(point_gpx.extensions) > 0:
                        for ext in point_gpx.extensions[0]:
                            if ext.tag == f'{NAMESPACE}cad':
                                trackpoint.cadence = int(ext.text)
                            elif ext.tag == f'{NAMESPACE}hr':
                                trackpoint.hr_value = int(ext.text)
                    points.append(trackpoint)
                    if previous_point is None:
                        trackpoint.distance = 0
                        trackpoint.speed = 0
                    else:
                        trackpoint.distance = (
                            previous_point.distance
                            + geopy.distance.geodesic(
                                (trackpoint.latitude, trackpoint.longitude),
                                (
                                    previous_point.latitude,
                                    previous_point.longitude,
                                ),
                            ).m
                        )
                        travelled = (
                            trackpoint.distance - previous_point.distance
                        )
                        if trackpoint.time is not None:
                            seconds_between = (
                                trackpoint.time - previous_point.time
                            ).total_seconds()
                            if (
                                seconds_between == 0
                            ):  # If two same timestamps, speed
                                # of previous timestamp is taken
                                trackpoint.speed = previous_point.speed
                            else:
                                trackpoint.speed = (
                                    travelled * 3.6 / seconds_between
                                )
                        else:
                            trackpoint.speed = 0
                    previous_point = trackpoint

        gpx_file.close()
        # handling missing data - should be improved in original
        try:
            activity_type = gpx.tracks[0].type
        except BaseException:
            activity_type = None

        positions = []
        altitudes = []
        distances = []
        timestamps = []
        heartrates = []
        speeds = []
        trackpoint: TCXTrackPoint
        for trackpoint in points:
            positions.append((trackpoint.latitude, trackpoint.longitude))
            altitudes.append(trackpoint.elevation)
            distances.append(trackpoint.distance)
            timestamps.append(trackpoint.time)
            speeds.append(trackpoint.speed)
            heartrates.append(trackpoint.hr_value)

        try:
            total_distance = distances[-1]
        except BaseException:
            total_distance = None

        if numpy_array is True:
            positions = np.array(positions)
            altitudes = np.array(altitudes)
            distances = np.array(distances)
            timestamps = np.array(timestamps)
            heartrates = np.array(heartrates)
            speeds = np.array(speeds)

        activity = {
            'activity_type': activity_type,
            'positions': positions,
            'altitudes': altitudes,
            'distances': distances,
            'total_distance': total_distance,
            'timestamps': timestamps,
            'heartrates': heartrates,
            'speeds': speeds,
        }

        return activity

    def extract_integral_metrics(self, filename) -> dict:
        """Method for parsing one GPX file and extracting integral metrics.\n
        Returns: int_metrics: {
                    "activity_type": activity_type,
                    "distance": distance,
                    "duration": duration,
                    "calories": calories,
                    "hr_avg": hr_avg,
                    "hr_max": hr_max,
                    "hr_min": hr_min,
                    "altitude_avg": altitude_avg,
                    "altitude_max": altitude_max,
                    "altitude_min": altitude_min,
                    "ascent": ascent,
                    "descent": descent,
                }.
        """
        gpx = self.read_one_file(filename)

        # handling missing data in raw files
        try:
            activity_type = gpx.tracks[0].type
        except BaseException:
            activity_type = None

        try:
            distance = gpx['total_distance']
        except BaseException:
            distance = None

        try:
            duration = gpx['timestamps'][-1] - gpx['timestamps'][0]
        except BaseException:
            duration = None

        try:
            calories = None
        except BaseException:
            calories = None

        try:
            hr_avg = sum(gpx['heartrates']) / len(gpx['heartrates'])
        except BaseException:
            hr_avg = None

        try:
            hr_max = max(gpx['heartrates'])
        except BaseException:
            hr_max = None

        try:
            hr_min = min(gpx['heartrates'])
        except BaseException:
            hr_min = None

        try:
            altitude_avg = sum(gpx['altitudes']) / len(gpx['altitudes'])
        except BaseException:
            altitude_avg = None

        try:
            altitude_max = max(gpx['altitudes'])
        except BaseException:
            altitude_max = None

        try:
            altitude_min = min(gpx['altitudes'])
        except BaseException:
            altitude_min = None

        try:
            ascent = self.__ascent(gpx['altitudes'])
        except BaseException:
            ascent = None

        try:
            descent = self.__descent(gpx['altitudes'])
        except BaseException:
            descent = None

        int_metrics = {
            'activity_type': activity_type,
            'distance': distance,
            'duration': duration,
            'calories': calories,
            'hr_avg': hr_avg,
            'hr_max': hr_max,
            'hr_min': hr_min,
            'altitude_avg': altitude_avg,
            'altitude_max': altitude_max,
            'altitude_min': altitude_min,
            'ascent': ascent,
            'descent': descent,
        }
        return int_metrics
