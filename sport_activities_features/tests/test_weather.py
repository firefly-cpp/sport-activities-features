import os
from unittest import TestCase
from sport_activities_features import TCXFile, WeatherIdentification
import pickle

class TestWeather(TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "data", "15.tcx")
        weather_external_data = os.path.join(os.path.dirname(__file__), "data", "weather_test.temp")
        tcx_file=TCXFile()
        self.data = tcx_file.read_one_file(filename)
        self.weather = None
        with open(weather_external_data, "rb") as input:
            self.weather=pickle.load(input)

    def test_average_weather_size(self):
        avg_weather = WeatherIdentification.get_average_weather_data(timestamps=self.data['timestamps'], weather=self.weather)
        self.assertEqual(len(avg_weather), 7799)

    def test_average_weather_between_two_timestamps(self):
        avg_weather = WeatherIdentification.get_average_weather_data(timestamps=self.data['timestamps'], weather=self.weather)
        self.assertAlmostEqual(avg_weather[38].temperature, 7.807, 2)
        self.assertAlmostEqual(avg_weather[38].sea_level_pressure, 994.063, 2)
        self.assertAlmostEqual(avg_weather[38].dew_point, -1.250, 2)
        self.assertAlmostEqual(avg_weather[38].wind_direction, 103.868, 2)

