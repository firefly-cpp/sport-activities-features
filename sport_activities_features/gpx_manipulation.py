import datetime

from tcxreader.tcxreader import TCXExercise, TCXTrackPoint, TCXReader
import gpxpy
import os
import geopy


class GPXTrackPoint():
    def __init__(self, longitude: float = None, latitude: float = None, elevation: float = None, time=None,
                 distance=None, hr_value: int = None, cadence=None, watts: float = None, speed: float = None):
        self.elevation = elevation
        self.latitude = latitude
        self.longitude = longitude
        self.time = time
        self.speed = speed
        self.distance = distance
        self.hr_value = hr_value
        self.cadence = cadence
        self.watts = watts

    def from_GPX(self, gpx: gpxpy.gpx.GPXTrackPoint, hr_value: int = None, cadence: int = None, watts: int = None):
        self.elevation = gpx.elevation
        self.latitude = gpx.latitude
        self.longitude = gpx.longitude
        self.time = gpx.time
        self.hr_value = hr_value
        self.cadence = cadence
        self.watts = watts


class GPXFile(object):
    r"""Working with GPX files"""

    def __init__(self):
        self.all_files = []

    def read_directory(self, directory_name):
        r"""Find all tcx files in a directory.

        Returns:
            str: Array of strings
        """

        files = os.listdir(directory_name)
        all_files1 = [i for i in files if i.endswith(".gpx")]
        for j in range(len(all_files1)):
            file = os.path.join(directory_name, all_files1[j])
            self.all_files.append(file)
        return self.all_files

    def read_one_file(self, filename):
        r"""Parse one GPX file.

        Returns:
            dictionary:

        Note:
            In the case of missing value in raw data, we assign None
        """
        NAMESPACE = "{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}"
        points = []
        lines = []
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
                    if previous_point==None:
                        trackpoint.distance=0
                        trackpoint.speed = 0
                    else:
                        trackpoint.distance = previous_point.distance+geopy.distance.geodesic((trackpoint.latitude, trackpoint.longitude), (previous_point.latitude, previous_point.longitude)).m
                        seconds_between = (trackpoint.time - previous_point.time).total_seconds()
                        travelled = trackpoint.distance-previous_point.distance
                        trackpoint.speed=travelled*3.6/seconds_between
                    previous_point=trackpoint

        gpx_file.close()
        # handling missing data - should be improved in original
        try:
            activity_type = gpx.activity_type
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
            a=100
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

        activity = {
            "activity_type": activity_type,
            "positions": positions,
            "altitudes": altitudes,
            "distances": distances,
            "total_distance": total_distance,
            "timestamps": timestamps,
            "heartrates": heartrates,
            "speeds":speeds
        }

        return activity

    def extract_integral_metrics(self, filename):
        r"""Parse one GPX file and extract integral metrics.

        Returns:
            dictionary:
        """
        tcx = TCXReader().read(filename)

        # handling missing data in raw files
        try:
            activity_type = tcx.activity_type
        except BaseException:
            activity_type = None

        try:
            distance = tcx.distance
        except BaseException:
            distance = None

        try:
            duration = tcx.duration
        except BaseException:
            duration = None

        try:
            calories = tcx.calories
        except BaseException:
            calories = None

        try:
            hr_avg = tcx.hr_avg
        except BaseException:
            hr_avg = None

        try:
            hr_max = tcx.hr_max
        except BaseException:
            hr_max = None

        try:
            hr_min = tcx.hr_min
        except BaseException:
            hr_min = None

        try:
            altitude_avg = tcx.altitude_avg
        except BaseException:
            altitude_avg = None

        try:
            altitude_max = max(tcx.trackpoints)
        except BaseException:
            altitude_max = None

        try:
            altitude_min = tcx.altitude_min
        except BaseException:
            altitude_min = None

        try:
            ascent = tcx.ascent
        except BaseException:
            ascent = None

        try:
            descent = tcx.descent
        except BaseException:
            descent = None

        int_metrics = {
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
        }
        return int_metrics
