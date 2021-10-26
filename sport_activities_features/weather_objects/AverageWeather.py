import datetime
from sport_activities_features.weather_objects.Weather import Weather
class AveragedType:
    def __init__(self, name, percentage):
        self.name = name
        self.percentage = percentage

def none_to_zero(value):
    if value==None:
        return 0
    else:
        return value

def weather_none_to_zero(weather:Weather):
    w=weather
    w.temperature = none_to_zero(w.temperature)
    w.maximum_temperature = none_to_zero(w.maximum_temperature)
    w.minimum_temperature = none_to_zero(w.minimum_temperature)
    w.wind_chill = none_to_zero(w.wind_chill)
    w.heat_index = none_to_zero(w.heat_index)
    w.solar_radiation = none_to_zero(w.solar_radiation)
    w.precipitation = none_to_zero(w.precipitation)
    w.sea_level_pressure = none_to_zero(w.sea_level_pressure)
    w.snow_depth = none_to_zero(w.snow_depth)
    w.wind_speed = none_to_zero(w.wind_speed)
    w.wind_direction = none_to_zero(w.wind_direction)
    w.wind_gust = none_to_zero(w.wind_gust)
    w.visibility = none_to_zero(w.visibility)
    w.cloud_cover = none_to_zero(w.cloud_cover)
    w.relative_humidity = none_to_zero(w.relative_humidity)
    w.dew_point = none_to_zero(w.dew_point)
    return w

class AverageWeather:
    """
    Class for providing average weather from two Weather objects
    """
    def __init__(
        self,
        weather_a: Weather = None,
        weather_b: Weather = None,
        weight_a = None,
    ):
        """
        Returns average weather between two dates (e.g. average temperature between two times)
        Args:
            weather_a:
            weather_b:
            weight_a:
        """
        a=weather_none_to_zero(weather_a)
        b=weather_none_to_zero(weather_b)
        weight_b=1-weight_a

        self.temperature = a.temperature*weight_a+b.temperature*weight_b
        self.maximum_temperature = a.maximum_temperature*weight_a+b.maximum_temperature*weight_b
        self.minimum_temperature = a.minimum_temperature*weight_a+b.minimum_temperature*weight_b
        #self.wind_chill = a.wind_chill*weight_a+b.wind_chill*weight_b EXCLUDED
        #self.heat_index = a.heat_index*weight_a+b.heat_index*weight_b EXCLUDED
        #self.solar_radiation = a.solar_radiation*weight_a+b.solar_radiation*weight_b EXCLUDED
        self.precipitation = a.precipitation*weight_a+b.solar_radiation*weight_b
        self.sea_level_pressure = a.sea_level_pressure*weight_a+b.solar_radiation*weight_b
        #self.snow_depth = a.snow_depth*weight_a+b.solar_radiation*weight_b EXCLUDED
        self.wind_speed = a.wind_speed*weight_a+b.solar_radiation*weight_b
        self.wind_direction = a.wind_direction*weight_a+b.solar_radiation*weight_b
        # self.wind_gust = a.wind_gust*weight_a+b.solar_radiation*weight_b EXCLUDED
        self.visibility = a.visibility*weight_a+b.solar_radiation*weight_b
        self.cloud_cover = a.cloud_cover*weight_a+b.solar_radiation*weight_b
        self.relative_humidity = a.relative_humidity*weight_a+b.solar_radiation*weight_b
        self.dew_point = a.dew_point*weight_a+b.solar_radiation*weight_b
        self.weather_type = [AveragedType(name=a.weather_type, percentage=weight_a),
                             AveragedType(name=b.weather_type, percentage=weight_b)] ###
        self.conditions = [AveragedType(name=a.conditions, percentage=weight_a),
                           AveragedType(name=b.conditions, percentage=weight_b)]



