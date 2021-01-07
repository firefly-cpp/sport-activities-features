import os
from .classes import StoredSegments
import requests
from sport_activities_features.tcx_manipulation import TCXFile
from datetime import datetime, timedelta


class Weather:
    def __init__(self, temperature: float = None, maximum_temperature: float = None, minimum_temperature: float = None,
                 wind_chill: float = None, heat_index: float = None, precipitation: float = None,
                 snow_depth: float = None, wind_speed: float = None, wind_gust=None, visibility: float = None,
                 cloud_cover: float = None, relative_humidity: float = None, weather_type: str = None,
                 conditions: str = None, date: datetime = None, location=None, index:int= None):
        self.temperature: float = temperature
        self.maximum_temperature = maximum_temperature
        self.minimum_temperature = minimum_temperature
        self.wind_chill = wind_chill
        self.heat_index = heat_index
        self.precipitation = precipitation
        self.snow_depth = snow_depth
        self.wind_speed = wind_speed
        self.wind_gust = wind_gust
        self.visibility = visibility
        self.cloud_cover = cloud_cover
        self.relative_humidity = relative_humidity
        self.weather_type = weather_type
        self.conditions = conditions
        self.date = date
        self.location = location
        self.index = index


class WeatherIdentification(object):
    r"""Identification of Weather data from TCX file.
        Attributes:
                altitudes: An array of altitude values extracted from TCX file
                ascent_threshold (float): Parameter that defines the hill (hill >= ascent_threshold)
        """

    def __init__(self, locations, timestamps, vc_api_key, unit_group="metric"):
        """
        Args:
            locations: list of locations from TCXFile.read_one_file() method
            timestamps: list of timestamps from TCXFile.read_one_file() method
            vc_api_key: VisualCrossing API key (https://www.visualcrossing.com/)
            unit_group: format of measurements. Possible values: 'us', 'metric', 'uk', 'base' (From: https://www.visualcrossing.com/resources/documentation/weather-api/unit-groups-and-measurement-units/)
        """
        self.locations = locations
        self.timestamps = timestamps
        self.vc_api_key = vc_api_key
        self.unit_group = unit_group

    def get_weather(self) -> [Weather]:
        """
        Returns: list of objects Weather from the nearest meteorological station for every 1 hour of training.
        """
        time = datetime(1980, 1, 1)
        weather_list: [Weather] = []
        index = 0

        for index in range(len(self.locations)):
            if time == datetime(1980, 1, 1):
                time = self.timestamps[index]
                location = (self.locations[index][0], self.locations[index][1])
                weather_response = self.weather_api_call(time, location,index)
                weather_list.append(weather_response)
            elif time + timedelta(minutes=60) < self.timestamps[index]:
                time = self.timestamps[index]
                location = (self.locations[index][0], self.locations[index][1])
                weather_response = self.weather_api_call(time, location, index)
                weather_list.append(weather_response)
        return weather_list


    def weather_api_call(self, time: datetime, location: (float, float), index):
        URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?"
        time_start = time.strftime('%Y-%m-%dT%H:%M:%S')
        time_end = (time + timedelta(hours=1, seconds=0)).strftime('%Y-%m-%dT%H:%M:%S')
        location0_str = "{:.5f}".format(location[0])
        location1_str = "{:.5f}".format(location[1])

        PARAMS = {'aggregateHours': 1, 'combinationMethod': 'aggregate', 'startDateTime': time_start,
                  'endDateTime': time_start, 'maxStations': -1, 'maxDistance': -1, 'contentType': 'json',
                  'unitGroup': self.unit_group, 'locationMode': 'single', 'key': self.vc_api_key,
                  'dataElements': 'default', 'locations': f'{location0_str}, {location1_str}'}
        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)
        # extracting data in json format
        data = r.json()
        data_values = data['location']['values'][0]
        return Weather(temperature=data_values['temp'], maximum_temperature=data_values['maxt'],
                       minimum_temperature=data_values['mint'], wind_chill=data_values['windchill'],
                       heat_index=data_values['heatindex'], precipitation=data_values['precip'],
                       snow_depth=data_values['snowdepth'], wind_speed=data_values['wspd'],
                       visibility=data_values['visibility'], cloud_cover=data_values['cloudcover'],
                       relative_humidity=data_values['humidity'], weather_type=data_values['weathertype'],
                       conditions=data_values['conditions'], date=time, location=location, index=index)

