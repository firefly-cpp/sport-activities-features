import datetime
class Weather:
    def __init__(self, temperature: float = None, maximum_temperature: float = None, minimum_temperature: float = None,
                 wind_chill: float = None, heat_index: float = None, precipitation: float = None,
                 snow_depth: float = None, wind_speed: float = None, wind_direction=None, wind_gust=None,
                 visibility: float = None,
                 cloud_cover: float = None, relative_humidity: float = None, weather_type: str = None,
                 sea_level_pressure=None, dew_point=None, solar_radiation=None,
                 conditions: str = None, date: datetime = None, location=None, index: int = None):
        self.temperature: float = temperature
        self.maximum_temperature = maximum_temperature
        self.minimum_temperature = minimum_temperature
        self.wind_chill = wind_chill
        self.heat_index = heat_index
        self.solar_radiation = solar_radiation
        self.precipitation = precipitation
        self.sea_level_pressure = sea_level_pressure
        self.snow_depth = snow_depth
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.wind_gust = wind_gust
        self.visibility = visibility
        self.cloud_cover = cloud_cover
        self.relative_humidity = relative_humidity
        self.dew_point = dew_point
        self.weather_type = weather_type
        self.conditions = conditions
        self.date = date
        self.location = location
        self.index = index
