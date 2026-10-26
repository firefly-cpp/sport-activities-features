import os
import tempfile
from unittest import TestCase

from sport_activities_features import GPXFile


class TestGPXFile(TestCase):
    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__), 'data', 'riderx3.gpx',
        )
        self.gpx_file = GPXFile()
        gpx_exercise = self.gpx_file.read_one_file(filename)
        self.data = self.gpx_file.extract_activity_data(gpx_exercise)

    def test_total_distance(self):
        self.assertAlmostEqual(self.data['total_distance'], 5774.703, 2)

    def test_number_of_positions(self):
        assert len(self.data['positions']) == 931

    def test_heartrates(self):
        assert self.data['heartrates'][0] == 107
        assert self.data['heartrates'][1] == 106

    def test_utf8_formatting(self):
        utf8_filenames = [
            'broken1.gpx',
            'broken2.gpx',
            'broken3.gpx',
            'broken4.gpx',
            'broken5.gpx',
        ]
        utf8_distances = [
            27060.581619705063,
            33440.56224468814,
            33759.501685168645,
            33689.54802374273,
            19086.306482072534,
        ]
        for index, f in enumerate(utf8_filenames):
            filename = os.path.join(os.path.dirname(__file__), 'data', f)
            gpx_exercise = self.gpx_file.read_one_file(filename)
            data = self.gpx_file.extract_activity_data(gpx_exercise)
            self.assertAlmostEqual(
                data['total_distance'], utf8_distances[index], places=5,
            )


class TestGPXExerciseSummary(TestCase):
    """Summary values of riderx3.gpx, checked against gpxpy and against
    the extracted trackpoint data."""

    def setUp(self):
        filename = os.path.join(
            os.path.dirname(__file__), 'data', 'riderx3.gpx',
        )
        self.gpx_file = GPXFile()
        self.exercise = self.gpx_file.read_one_file(filename)
        self.data = self.gpx_file.extract_activity_data(self.exercise)
        self.metrics = self.gpx_file.extract_integral_metrics(self.exercise)

    def test_integral_metrics(self):
        self.assertEqual(self.metrics['activity_type'], 'cycling')
        self.assertAlmostEqual(self.metrics['distance'], 5774.703, places=2)
        self.assertEqual(self.metrics['duration'], 2469.0)
        self.assertIsNone(self.metrics['calories'])
        self.assertAlmostEqual(self.metrics['hr_avg'], 141.8346, places=3)
        self.assertEqual(self.metrics['hr_max'], 171)
        self.assertEqual(self.metrics['hr_min'], 86)
        self.assertAlmostEqual(self.metrics['altitude_avg'], 395.483, places=2)
        self.assertAlmostEqual(self.metrics['altitude_max'], 555.0)
        self.assertAlmostEqual(self.metrics['altitude_min'], 197.8, places=3)
        self.assertAlmostEqual(self.metrics['ascent'], 331.6, places=2)
        self.assertAlmostEqual(self.metrics['descent'], 364.4, places=2)

    def test_matches_gpxpy(self):
        raw = self.exercise.raw_data
        self.assertEqual(self.exercise.duration, raw.get_duration())
        extremes = raw.get_elevation_extremes()
        self.assertAlmostEqual(self.exercise.altitude_min, extremes.minimum)
        self.assertAlmostEqual(self.exercise.altitude_max, extremes.maximum)
        self.assertAlmostEqual(
            self.exercise.distance, raw.length_2d(), delta=0.001 * raw.length_2d(),
        )

    def test_matches_extracted_data(self):
        self.assertEqual(self.exercise.distance, self.data['total_distance'])
        heartrates = [hr for hr in self.data['heartrates'] if hr is not None]
        self.assertAlmostEqual(
            self.exercise.hr_avg, sum(heartrates) / len(heartrates),
        )
        altitudes = self.data['altitudes']
        self.assertAlmostEqual(
            self.exercise.ascent - self.exercise.descent,
            altitudes[-1] - altitudes[0],
        )


class TestGPXExerciseMissingData(TestCase):
    """A GPX file with positions only: no time, elevation or heart rate."""

    gpx = '''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="test" xmlns="http://www.topografix.com/GPX/1/1">
  <trk><trkseg>
    <trkpt lat="46.000" lon="15.000"></trkpt>
    <trkpt lat="46.001" lon="15.000"></trkpt>
    <trkpt lat="46.002" lon="15.000"></trkpt>
  </trkseg></trk>
</gpx>
'''

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        filename = os.path.join(self.directory.name, 'route.gpx')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(self.gpx)
        self.exercise = GPXFile().read_one_file(filename)

    def tearDown(self):
        self.directory.cleanup()

    def test_missing_values_are_none(self):
        self.assertIsNone(self.exercise.activity_type)
        self.assertIsNone(self.exercise.duration)
        self.assertIsNone(self.exercise.hr_avg)
        self.assertIsNone(self.exercise.hr_max)
        self.assertIsNone(self.exercise.hr_min)
        self.assertIsNone(self.exercise.altitude_avg)
        self.assertIsNone(self.exercise.ascent)
        self.assertIsNone(self.exercise.descent)

    def test_distance(self):
        # Two steps of 0.001 degree of latitude, ~111 m each.
        self.assertAlmostEqual(self.exercise.distance, 222.4, delta=0.5)


class TestGPXExerciseAllSampleFiles(TestCase):
    def test_summary_values(self):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        filenames = sorted(
            name for name in os.listdir(data_dir) if name.endswith('.gpx')
        )
        self.assertGreaterEqual(len(filenames), 6)
        for name in filenames:
            with self.subTest(name):
                gpx_file = GPXFile()
                exercise = gpx_file.read_one_file(os.path.join(data_dir, name))
                data = gpx_file.extract_activity_data(exercise)
                self.assertEqual(exercise.distance, data['total_distance'])
                self.assertGreater(exercise.duration, 0)
                self.assertIsNotNone(exercise.altitude_avg)
                self.assertGreaterEqual(exercise.ascent, 0)
                self.assertLessEqual(
                    exercise.altitude_min, exercise.altitude_max,
                )
