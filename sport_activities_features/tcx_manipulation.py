import os
from tcxreader.tcxreader import TCXTrackPoint, TCXReader


class TCXFile(object):
    """
    Class for reading TCX files.
    """
    def __init__(self) -> None:
        """
        Initialisation method of TCXFile class.
        """
        self.all_files = []

    def read_directory(self, directory_name: str) -> list:
        """
        Method for finding all TCX files in a directory.\n
        Args:
            directory_name (str):
                name of the directory in which to identify TCX files
        Returns:
            str: array of paths to the identified files
        """
        files = os.listdir(directory_name)
        all_files1 = [i for i in files if i.endswith(".tcx")]
        for j in range(len(all_files1)):
            file = os.path.join(directory_name, all_files1[j])
            self.all_files.append(file)
        return self.all_files

    def read_one_file(self, filename: str) -> dict:
        """
        Method for parsing one TCX file using the TCXReader.\n
        Args:
            filename (str):
                name of the TCX file to be read
        Returns:
            activity = {
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
        tcx = TCXReader().read(filename)

        # handling missing data - should be improved in original tcxparser
        try:
            activity_type = tcx.activity_type
        except BaseException:
            activity_type = None

        positions = []
        altitudes = []
        distances = []
        timestamps = []
        heartrates = []
        speeds = []
        trackpoint: TCXTrackPoint

        invalid_points = []
        for index, trackpoint in enumerate(tcx.trackpoints):
            positions.append((trackpoint.latitude, trackpoint.longitude))
            altitudes.append(trackpoint.elevation)
            distances.append(trackpoint.distance)
            timestamps.append(trackpoint.time)
            heartrates.append(trackpoint.hr_value)
            if index != 0:
                delta_distance = distances[-1] - distances[-2]
                delta_time = (timestamps[-1] - timestamps[-2]).total_seconds()
                if (delta_time == 0):
                    delta_time = 1
                    delta_distance = 1
                    invalid_points.append(index)
                speeds.append((delta_distance / delta_time) * 3.6)
            else:
                speeds.append(0)

        if len(invalid_points) > 0:
            print(
                'Probably invalid speeds or not a record of exercise.',
                f'Invalid trackpoints count: {len(invalid_points)}',
                f'Filename:{filename}'
            )

        try:
            total_distance = tcx.distance
        except BaseException:
            total_distance = None

        activity = {
            'activity_type': activity_type,
            'positions': positions,
            'altitudes': altitudes,
            'distances': distances,
            'total_distance': total_distance,
            'timestamps': timestamps,
            'heartrates': heartrates,
            'speeds': speeds
        }
        return activity

    def extract_integral_metrics(self, filename: str) -> dict:
        """
        Method for parsing one TCX file and extracting integral metrics.\n
        Args:
            filename (str):
                name of the TCX file to be read
        Returns:
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
                'steps' : steps
            }
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

        try:
            steps = tcx.steps
        except BaseException:
            steps = None
            
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
            'steps' : steps,
        }
        return int_metrics
