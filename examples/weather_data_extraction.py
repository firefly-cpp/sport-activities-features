from sport_activities_features import WeatherIdentification
from sport_activities_features import TCXFile

#read TCX file
tcx_file = TCXFile()
tcx_data = tcx_file.read_one_file("datasets\\15.tcx")

#configure visual crossing api key
visual_crossing_api_key = "weather_api_key" # https://www.visualcrossing.com/weather-api

# Explanation of elements - https://www.visualcrossing.com/resources/documentation/weather-data/weather-data-documentation/
weather = WeatherIdentification(tcx_data['positions'], tcx_data['timestamps'], visual_crossing_api_key)
weatherlist = weather.get_weather(time_delta=30)
tcx_weather = weather.get_average_weather_data(timestamps=tcx_data['timestamps'],weather=weatherlist)
#add weather to TCX data
tcx_data.update({'weather':tcx_weather})
