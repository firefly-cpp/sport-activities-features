import os
from typing import TYPE_CHECKING

import geopy
import gpxpy
import gpxpy.gpx
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
        from the gpxpy.gpx.GPXTrackPoint.\n
        Args:
            gpx (gpxpy.gpx.GPXTrackPoint):
                gpxpy.gpx.GPXTrackPoint to extract data from
            hr_value (int):
                heart beats per minute at given recording
            cadence (int):
                cadence
            watts (int):
                watts power rating.
        Note:
            Parameter gpx and its type gpxpy.gpx.GPXTrackPoint should not be confused with the class of the same name used in gpx_manipulation
        """
        self.elevation = gpx.elevation
        self.latitude = gpx.latitude
        self.longitude = gpx.longitude
        self.time = gpx.time
        self.hr_value = hr_value
        self.cadence = cadence
        self.watts = watts

class GPXExercise:
    """Class for storing exercise data from a GPX file.\n
    Args:
        raw_data (GPX):
            raw data from the GPX file.
        trackpoints (list):
            list of GPXTrackPoint objects.        
        activity_type (str):
            type of the activity (e.g. Biking).
        distance (float):
            total distance of exercise in meters.
        duration (float):
            duration of exercise in seconds.
        calories (int):
            calories burned during the exercise.
        hr_avg (float):
            average heart rate during the exercise.
        hr_max (int):
            maximum heart rate during the exercise.
        hr_min (int):
            minimum heart rate during the exercise.
        altitude_avg (float):
            average altitude in meters.
        altitude_max (float):
            maximum altitude in meters.
        altitude_min (float):
            minimum altitude in meters.
        ascent (float):
            total ascent in meters.
        descent (float):
            total descent in meters.
    """

    def __init__(self, raw_data: gpxpy.gpx.GPX, trackpoints: list = None) -> None:
        """Initialisation method for GPXExercise class.\n
        Args:
            raw_data (GPX):
                raw data from the GPX file.
            trackpoints (list):
                list of GPXTrackPoint objects.
        """
        if trackpoints is None:
            trackpoints = []
        self.trackpoints = trackpoints
        self.raw_data = raw_data
        self._calculate_values()
        
    def _calculate_values(self):
        gpx = self.raw_data
        try:
            self.activity_type = gpx.tracks[0].type
        except BaseException:
            self.activity_type = None

        try:
            self.distance = gpx['total_distance']
        except BaseException:
            self.distance = None

        try:
            self.duration = gpx['timestamps'][-1] - gpx['timestamps'][0]
        except BaseException:
            self.duration = None

        try:
            self.calories = None
        except BaseException:
            self.calories = None

        try:
            self.hr_avg = sum(gpx['heartrates']) / len(gpx['heartrates'])
        except BaseException:
            self.hr_avg = None

        try:
            self.hr_max = max(gpx['heartrates'])
        except BaseException:
            self.hr_max = None

        try:
            self.hr_min = min(gpx['heartrates'])
        except BaseException:
            self.hr_min = None

        try:
            self.altitude_avg = sum(gpx['altitudes']) / len(gpx['altitudes'])
        except BaseException:
            self.altitude_avg = None

        try:
            self.altitude_max = max(gpx['altitudes'])
        except BaseException:
            self.altitude_max = None

        try:
            self.altitude_min = min(gpx['altitudes'])
        except BaseException:
            self.altitude_min = None

        try:
            self.ascent = self.__ascent(gpx['altitudes'])
        except BaseException:
            self.ascent = None

        try:
            self.descent = self.__descent(gpx['altitudes'])
        except BaseException:
            self.descent = None
            
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


class GPXFile(FileManipulation):
    """Class for reading GPX files."""

    def __init__(self) -> None:
        """Initialisation method for GPXFile class."""
        self.all_files = []
   

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

    def read_one_file(self, filename: str) -> GPXExercise:
        """Method for parsing one GPX file.\n
        Args:
            filename (str):
                name of the TCX file to be read
        Returns:
          activity (dict):
            {
                'activity_type': activity_type,
                'positions': positions,
                'altitudes': altitudes,
                'distances': distances,
                'total_distance': total_distance,
                'timestamps': timestamps,
                'heartrates': heartrates,
                'speeds': speeds
            }

        Note:        
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
        gpx_exercise = GPXExercise(gpx,points)
        return gpx_exercise


    def extract_activity_data(self, gpx: GPXExercise, numpy_array = False) -> dict:
        """Method for parsing one GPX file.\n
        Args:
            gpx (GPXExercise):
                GPXExercise object to be read
            numpy_array (bool):
                if True, dictionary lists are transformed into numpy arrays
        Returns:
          activity (dict):
            {
                'activity_type': activity_type,
                'positions': positions,
                'altitudes': altitudes,
                'distances': distances,
                'total_distance': total_distance,
                'timestamps': timestamps,
                'heartrates': heartrates,
                'speeds': speeds
            }

        Note:        
            In the case of missing value in raw data, we assign None.
        """
        # handling missing data - should be improved in original
        try:
            activity_type = gpx.raw_data.tracks[0].type
        except BaseException:
            activity_type = None

        positions = []
        altitudes = []
        distances = []
        timestamps = []
        heartrates = []
        speeds = []
        trackpoint: GPXTrackPoint
        for trackpoint in gpx.trackpoints:
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
    
    def extract_integral_metrics(self, gpx_exercise: GPXExercise) -> dict:
        """Method for parsing one GPX file and extracting integral metrics.\n
        Args:
            filename (str):
                name of the GPX file to be read
        Returns:
          int_metrics (dict): 
            {
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

        # handling missing data in raw files
        try:
            activity_type = gpx_exercise.activity_type
        except BaseException:
            activity_type = None

        try:
            distance = gpx_exercise.distance
        except BaseException:
            distance = None

        try:
            duration = gpx_exercise.duration
        except BaseException:
            duration = None

        try:
            calories = gpx_exercise.calories
        except BaseException:
            calories = None

        try:
            hr_avg = gpx_exercise.hr_avg
        except BaseException:
            hr_avg = None

        try:
            hr_max = gpx_exercise.hr_max
        except BaseException:
            hr_max = None

        try:
            hr_min = gpx_exercise.hr_min
        except BaseException:
            hr_min = None

        try:
            altitude_avg = gpx_exercise.altitude_avg
        except BaseException:
            altitude_avg = None

        try:
            altitude_max = gpx_exercise.altitude_max
        except BaseException:
            altitude_max = None

        try:
            altitude_min = gpx_exercise.altitude_min
        except BaseException:
            altitude_min = None

        try:
            ascent = gpx_exercise.ascent
        except BaseException:
            ascent = None

        try:
            descent = gpx_exercise.descent
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
