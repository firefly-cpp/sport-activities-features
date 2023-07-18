import os
from pathlib import Path

import numpy as np
from tcx2gpx import tcx2gpx
from tcxreader.tcxreader import TCXReader, TCXTrackPoint

from sport_activities_features.file_manipulation import FileManipulation


class TCXFile(FileManipulation):

    """Class for reading TCX files."""

    def __init__(self) -> None:
        """Initialisation method of TCXFile class."""
        self.all_files = []

    def read_directory(self, directory_name: str) -> list:
        """Method for finding all TCX files in a directory.\n
        Args:
            directory_name (str):
                name of the directory in which to identify TCX files
        Returns:
            str: array of paths to the identified files.
        """
        files = os.listdir(directory_name)
        all_files1 = [i for i in files if i.endswith('.tcx')]
        for j in range(len(all_files1)):
            file = os.path.join(directory_name, all_files1[j])
            self.all_files.append(file)
        return self.all_files

    def read_one_file(self, filename: str, numpy_array=False) -> dict:
        """Method for parsing one TCX file using the TCXReader.\n
        Args:
            filename (str):
                name of the TCX file to be read
            numpy_array (bool):
                if set to true dictionary lists are
                   transformed into numpy.arrays
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
            }.

        Note:
        ----
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

        for index, trackpoint in enumerate(tcx.trackpoints):
            if index != 0:
                delta_distance = trackpoint.distance - distances[-1]
                delta_time = (trackpoint.time - timestamps[-1]).total_seconds()
                if delta_time != 0:
                    heartrates.append(trackpoint.hr_value)
                    positions.append(
                        (trackpoint.latitude, trackpoint.longitude),
                    )
                    altitudes.append(trackpoint.elevation)
                    distances.append(trackpoint.distance)
                    timestamps.append(trackpoint.time)
                    speeds.append((delta_distance / delta_time) * 3.6)
            else:
                heartrates.append(trackpoint.hr_value)
                positions.append((trackpoint.latitude, trackpoint.longitude))
                altitudes.append(trackpoint.elevation)
                if trackpoint.distance is None:
                    distances.append(0)
                else:
                    distances.append(trackpoint.distance)
                timestamps.append(trackpoint.time)
                speeds.append(0)

        try:
            total_distance = tcx.distance
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
            'start_time': tcx.start_time,
        }
        return activity

    def extract_integral_metrics(self, filename: str) -> dict:
        """Method for parsing one TCX file and extracting integral metrics.\n
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
            }.
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
            altitude_max = tcx.altitude_max
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
            steps = tcx.lx_ext['Steps']
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
            'steps': steps,
        }
        return int_metrics

    def write_gpx(self, gps_object, output_file_name=None):
        """Write GPX object to file.
        if output_file_name is not specified,
        the output file name will be the same
        as the input file name,
        but with .gpx extension.
        """
        if output_file_name is None:
            output_file_name = str(gps_object.tcx_path.resolve()).replace(
                '.tcx', '.gpx',
            )

        with open(output_file_name, 'w') as output:
            output.write(gps_object.gpx.to_xml())

    def create_gps_object(self, path_to_the_file):
        """Convert TCX file to GPX file."""
        gps_object = tcx2gpx.TCX2GPX(tcx_path=path_to_the_file)
        gps_object.read_tcx()
        gps_object.extract_track_points()
        gps_object.create_gpx()
        return gps_object

    def convert_tcx_to_gpx(
        self, local_path_to_original_file: str, output_file_name=None,
    ):
        try:
            """
            This is a try-except block.
            First we create a Path objects from the local path
            Then we try to convert the file.
            If it fails, we try to fix the file and convert it.
            """
            local_path_to_original_file = Path(local_path_to_original_file)
            abs_path_to_directory = str(
                os.path.split(os.path.abspath(local_path_to_original_file))[0],
            )
            abs_path_to_original_file = str(
                Path(local_path_to_original_file).resolve(),
            )

            gps_object = self.create_gps_object(abs_path_to_original_file)
            if output_file_name is None:
                self.write_gpx(gps_object)
            else:
                output_file_name = (
                    abs_path_to_directory + '\\' + str(output_file_name)
                )
                self.write_gpx(gps_object, output_file_name)
            return gps_object

        except ValueError:
            try:
                """
                This is a try-except block.
                And simple naive fix for the file.
                Due to ISO 8601 standard, the Z in
                the end of the time string is not
                allowed to have milliseconds.
                """

                # Intermediate file
                if output_file_name is None:
                    path_to_the_fixed_file = str(
                        abs_path_to_original_file.replace('.tcx', '.gpx'),
                    )
                else:
                    path_to_the_fixed_file = (
                        abs_path_to_directory + '\\' + str(output_file_name)
                    )

                # Open original file to try fix and convert from tcx to gpx
                file_to_fix_convert = open(abs_path_to_original_file)

                # Output file - .gpx - to write the result to
                fixed_file = open(path_to_the_fixed_file, 'w')

                # For every line of the original file
                for line in file_to_fix_convert:
                    # Read and replace string, write to output file
                    fixed_file.write(line.replace('.000Z', 'Z'))

                # Close original and fixed file
                file_to_fix_convert.close()
                fixed_file.close()

                gps_object = self.create_gps_object(path_to_the_fixed_file)
                self.write_gpx(gps_object, path_to_the_fixed_file)

                return gps_object

            except ValueError:
                msg = 'Error in converting the file'
                raise ValueError(msg)
