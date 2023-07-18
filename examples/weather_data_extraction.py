from sport_activities_features import TCXFile, WeatherIdentification

# Read TCX file
tcx_file = TCXFile()
tcx_data = tcx_file.read_one_file('path_to_the_file')

# Configure visual crossing api key
# https://www.visualcrossing.com/weather-api
visual_crossing_api_key = 'weather_api_key'

# Explanation of elements
# https://www.visualcrossing.com/resources/documentation/weather-data/weather-data-documentation/
weather = WeatherIdentification(
    tcx_data['positions'],
    tcx_data['timestamps'],
    visual_crossing_api_key,
)
weatherlist = weather.get_weather(time_delta=30)
tcx_weather = weather.get_average_weather_data(
    timestamps=tcx_data['timestamps'],
    weather=weatherlist,
)

""" tcx_weather -> returns data of the following type
     [
        {
            'temperature': 14.3,
            'maximum_temperature': 14.3,
            'minimum_temperature': 14.3,
            'wind_chill': null,
            'heat_index': null,
            'solar_radiation': null,
            'precipitation': 0.0,
            'sea_level_pressure': 1021.6,
            'snow_depth': null,
            'wind_speed': 6.9,
            'wind_direction': 129.0,
            'wind_gust': null,
            'visibility': 40.0,
            'cloud_cover': 54.3,
            'relative_humidity': 47.6,
            'dew_point': 3.3,
            'weather_type': '',
            'conditions': 'Partially cloudy',
            'date': '2016-04-02T17:26:09+00:00',
            'location': [
                46.079871179535985,
                14.738618675619364
            ],
            'index': 0
        }, ...
    ]
"""

# Add weather to TCX data
tcx_data.update({'weather': tcx_weather})
