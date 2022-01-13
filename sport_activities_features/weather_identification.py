import requests
from sport_activities_features.tcx_manipulation import TCXFile
from datetime import datetime, timedelta

from sport_activities_features.weather_objects.AverageWeather import AverageWeather
from sport_activities_features.weather_objects.Weather import Weather



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

    def get_weather(self, time_delta=30) -> [Weather]:
        """
        Args:
            time_delta: time between two measurements, default 30 mins
        Returns: list of objects Weather from the nearest meteorological station for every 1 hour of training.

        """
        time = datetime(1980, 1, 1)
        weather_list: [Weather] = []
        index = 0

        for index in range(len(self.locations)):
            if time == datetime(1980, 1, 1):
                time = self.timestamps[index]
                location = (self.locations[index][0], self.locations[index][1])
                weather_response = self.weather_api_call(time, location, index)
                weather_list.append(weather_response)
            elif time + timedelta(minutes=time_delta) < self.timestamps[index]:
                time = self.timestamps[index]
                location = (self.locations[index][0], self.locations[index][1])
                weather_response = self.weather_api_call(time, location, index)
                weather_list.append(weather_response)

            if index == len(self.locations) - 1:
                time = self.timestamps[index] + timedelta(minutes=60)
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
                  'dataElements': 'all', 'locations': f'{location0_str}, {location1_str}'}
        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)
        # extracting data in json format
        data = r.json()
        data_values = data['location']['values'][0]
        return Weather(temperature=data_values['temp'], maximum_temperature=data_values['maxt'],
                       minimum_temperature=data_values['mint'], wind_chill=data_values['windchill'],
                       heat_index=data_values['heatindex'], precipitation=data_values['precip'],
                       snow_depth=data_values['snowdepth'], wind_speed=data_values['wspd'],
                       wind_direction=data_values['wdir'], sea_level_pressure=data_values['sealevelpressure'],
                       visibility=data_values['visibility'], cloud_cover=data_values['cloudcover'],
                       dew_point=data_values['dew'],
                       solar_radiation=data_values['solarradiation'],
                       relative_humidity=data_values['humidity'], weather_type=data_values['weathertype'],
                       conditions=data_values['conditions'], date=time, location=location, index=index)

    @classmethod
    def __find_nearest_weathers(self, timestamp, weather_list):
        beforeWeathers = list(filter(lambda x: timestamp >= x.date - timedelta(minutes=1), weather_list))
        afterWeathers = list(filter(lambda x: timestamp < x.date, weather_list))
        before = None
        beforeSeconds = 999999999999999999999999999
        after = None
        afterSeconds = 999999999999999999999999999

        for bw in beforeWeathers:
            t = timestamp - bw.date if timestamp > bw.date else bw.date - timestamp
            if beforeSeconds > t.seconds:
                before = bw
                beforeSeconds = t.seconds
        for aw in afterWeathers:
            t = timestamp - aw.date if timestamp > aw.date else aw.date - timestamp
            if afterSeconds > t.seconds:
                after = aw
                afterSeconds = t.seconds
        return {'before': {'weather': before, 'seconds': beforeSeconds},
                'after': {'weather': after, 'seconds': afterSeconds}}

    @classmethod
    def get_average_weather_data(self, timestamps, weather:[Weather]):
        """
        :param timestamps: Timestamps from read TCX file method
        :return: AverageWeather[], averaged out objects of weather
        """
        weather_list = weather
        extended_weather_list = []

        for timestamp in timestamps:
            before_after = self.__find_nearest_weathers(timestamp, weather_list)
            before = before_after['before']
            after = before_after['after']
            weight_a = 1 - (before['seconds'] / (after['seconds'] + before['seconds']))
            average_weather_at_timestamp = AverageWeather(weather_a=before['weather'],
                                                           weather_b=after['weather'],
                                                           weight_a=weight_a)
            extended_weather_list.append(average_weather_at_timestamp)

        return extended_weather_list