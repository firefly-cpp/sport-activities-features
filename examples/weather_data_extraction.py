from sport_activities_features.weather_identification import WeatherIdentification
from sport_activities_features.tcx_manipulation import TCXFile

# read TCX file
tcx_file = TCXFile()
tcx_data = tcx_file.read_one_file("path_to_the_file")

# configure visual crossing api key
visual_crossing_api_key = "API_KEY"  # https://www.visualcrossing.com/weather-api

# return weather objects
weather = WeatherIdentification(
    tcx_data["positions"], tcx_data["timestamps"], visual_crossing_api_key
)
weatherlist = weather.get_weather()
