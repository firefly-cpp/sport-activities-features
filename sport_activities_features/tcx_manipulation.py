from tcxreader.tcxreader import TCXExercise, TCXTrackPoint, TCXReader
import os


class TCXFile(object):
    r"""Working with TCX files
        """

    def __init__(self):
        self.all_files = []

    def read_directory(self, directory_name):
        r"""Find all tcx files in a directory.

                Returns:
                        str: Array of strings

                """

        files = os.listdir(directory_name)
        all_files1 = [i for i in files if i.endswith('.tcx')]
        for j in range(len(all_files1)):
            file = directory_name + all_files1[j]
            self.all_files.append(file)
        return self.all_files

    def read_one_file(self, filename):
        r"""Parse one TCX file.

                Returns:
                        dictionary:

        Note:
            In the case of missing value in raw data, we assign None
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
        trackpoint:TCXTrackPoint
        for trackpoint in tcx.trackpoints:
            positions.append((trackpoint.latitude, trackpoint.longitude))
            altitudes.append(trackpoint.elevation)
            distances.append(trackpoint.distance)
            timestamps.append(trackpoint.time)


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
            'timestamps':timestamps
        }
        
        return activity

    def extract_integral_metrics(self, filename):
        r"""Parse one TCX file and extract integral metrics.

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
            'descent': descent}
        return int_metrics
