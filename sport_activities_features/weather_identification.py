from datetime import datetime, timedelta

import requests

from sport_activities_features.weather_objects.AverageWeather import AverageWeather
from sport_activities_features.weather_objects.Weather import Weather


class WeatherIdentification(object):
    r"""A class used for identification of Weather data from TCX file.
    For identification of weather an external API is used (https://www.visualcrossing.com/).

    Args:
        locations : (float, float) coordinates of exercise recordings, found in TCXFile/GPXFile generated dictionary under "positions"
        timestamps : timestamps of exercise recordings, found in TCXFile/GPXFile generated dictionary under "timestamps"
        vc_api_key : API key for accessing VisualCrossing weather data
        unit_group : Unit group of data recieved. Possible options 'metric' (default), 'us', 'uk', 'base'.

    Warnings:
        vc_api_key : api key is required

    """

    def __init__(self, locations: [(float, float)], timestamps: [datetime], vc_api_key: str, unit_group="metric"):
        """
        Constructor for WeatherIdentification class
        Args:
            locations : [(float, float)] coordinates of exercise recordings, found in TCXFile/GPXFile generated dictionary under "positions"
            timestamps : [datetime] timestamps of exercise recordings, found in TCXFile/GPXFile generated dictionary under "timestamps"
            vc_api_key : API key for accessing VisualCrossing weather data
            unit_group : Unit group of data recieved. Possible options 'metric' (default), 'us', 'uk', 'base'.
        """
        self.locations: [(float, float)] = locations
        self.timestamps = timestamps
        self.vc_api_key = vc_api_key
        self.unit_group = unit_group

    def get_weather(self, time_delta: int = 30) -> [Weather]:
        """
        Queries the VisualCrossing weather API for meteorological data at provided (minute) time intervals.
        Args:
            time_delta : time between two measurements, default 30 mins
        Returns:
                [Weather] - list of Weather objects from the nearest meteorological station for every interval (time_delta minutes) of training.
        """
        time = datetime(1980, 1, 1)
        weather_list: [Weather] = []
        index = 0

        for index in range(len(self.locations)):
            if time == datetime(1980, 1, 1):
                time = self.timestamps[index]
                location = (self.locations[index][0], self.locations[index][1])
                weather_response = self.__weather_api_call(time, location, index)
                weather_list.append(weather_response)
            elif time + timedelta(minutes=time_delta) < self.timestamps[index]:
                time = self.timestamps[index]
                location = (self.locations[index][0], self.locations[index][1])
                weather_response = self.__weather_api_call(time, location, index)
                weather_list.append(weather_response)

            if index == len(self.locations) - 1:
                time = self.timestamps[index] + timedelta(minutes=60)
                location = (self.locations[index][0], self.locations[index][1])
                weather_response = self.__weather_api_call(time, location, index)
                weather_list.append(weather_response)

        return weather_list

    def __weather_api_call(self, time: datetime, location: (float, float), index):
        """
        Internal method for making a REST request to the VisualCrossing API.
        Args:
            time : Time at which we are interested in the weather
            location : (float, float) latitude, longitude of the training point for which we are interested in weather.
            index: Index of weather object. E.g. a training that lasts 90 min, time-delta 30. Would have Weather objects
                with indexes 0, 1, 2.

        Returns:
            Weather(): object of the weather at specified time and location.

        """
        URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?"
        time_start = time.strftime('%Y-%m-%dT%H:%M:%S')
        # time_end = (time + timedelta(hours=1, seconds=0)).strftime('%Y-%m-%dT%H:%M:%S')
        location0_str = "{:.5f}".format(location[0])
        location1_str = "{:.5f}".format(location[1])

        PARAMS = {'aggregateHours': 1, 'combinationMethod': 'aggregate', 'startDateTime': time_start,
                  'endDateTime': time_start, 'maxStations': -1, 'maxDistance': -1, 'contentType': 'json',
                  'unitGroup': self.unit_group, 'locationMode': 'single', 'key': self.vc_api_key,
                  'dataElements': 'all', 'locations': f'{location0_str}, {location1_str}'}
        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)
        # extracting data in json format
        response_data = r.json()
        data_values = response_data['location']['values'][0]
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
    def __find_nearest_weathers(self, timestamp: datetime, weather_list: [Weather]):
        """
        Finds the two nearest (before and after) Weather() objects from the provided weather_list.
        Args:
            timestamp : datetime timestamp that we are interested in.
            weather_list : [Weather] List of Weather objects from which we want to find the closest before and after Weather.

        Returns: dict : {'before': {'weather': before, 'seconds': beforeSeconds}, 'after': {'weather': after, 'seconds': afterSeconds}}
                Dictionary with two Weather objects (['before]['weather], ['after']['weather']) and two time measurements
                (['before']['seconds'], ['after']['seconds']) which tell how much time is between the given timestamp
                and the identified weather objects.

        """
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
    def get_average_weather_data(self, timestamps: [datetime], weather: [Weather]):
        """
        Generates average weather for each of the timestamps in training by averaging the weather before and after the
        timestamp, using the __find_nearest_weathers() method.

        Args:
            timestamps : [datetime] datetime recordings from the TCXFile parsed data
            weather: [Weather] list of weather objects retrieved from VisualCrossing API
        Returns:
            [AverageWeather] list which is an AverageWeather object for each of the given timestamps.

        """
        weather_list = weather
        extended_weather_list = []

        for timestamp in timestamps:
            before_after = self.__find_nearest_weathers(timestamp, weather_list)
            before = before_after['before']
            after = before_after['after']
            # Weight depends on the proximity to both of the nearest Weather objects so that weather can be averaged out.
            weight_a = 1 - (before['seconds'] / (after['seconds'] + before['seconds']))
            average_weather_at_timestamp = AverageWeather(weather_a=before['weather'],
                                                          weather_b=after['weather'],
                                                          weight_a=weight_a)
            extended_weather_list.append(average_weather_at_timestamp)

        return extended_weather_list
