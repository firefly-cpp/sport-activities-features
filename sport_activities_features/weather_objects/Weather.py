import datetime


class Weather:

    r"""A class for the Weather object files. Args reported
    based on VisualCrossing API description.
    """

    def __init__(
        self,
        temperature: float = None,
        maximum_temperature: float = None,
        minimum_temperature: float = None,
        wind_chill: float = None,
        heat_index: float = None,
        precipitation: float = None,
        snow_depth: float = None,
        wind_speed: float = None,
        wind_direction=None,
        wind_gust=None,
        visibility: float = None,
        cloud_cover: float = None,
        relative_humidity: float = None,
        weather_type: str = None,
        sea_level_pressure=None,
        dew_point=None,
        solar_radiation=None,
        conditions: str = None,
        date: datetime = None,
        location=None,
        index: int = None,
    ) -> None:
        """Initialisation method for Weather objects.

        Args:
        ----
            temperature : Average (mean) temperature
                          during the measuring period
            maximum_temperature : Maximum temperature during
                                  the measuring period
            minimum_temperature : Minimum temperature during
                                  the measuring period
            wind_chill : Bodily discomfort related to cold
                         temperature & wind
            heat_index : Bodily discomfort related to hot
                         temperature & humidity
            precipitation : Total amount of precipitation of
                            any type that fell during the
                            measuring period.
            snow_depth : Depth of snow on the ground
            wind_speed : The average wind speed over the past
                         two-minute time window before the report
            wind_direction : The average direction of the wind
                             during the wind speed reports.
                             The unit shows degrees from 1 to 360
                             in whole numbers.
                             90 equivalents to direction 'East'
                             180 to 'South', 270 to 'West'
                             and 360 to 'North'.
            wind_gust :
                Weather measure that is reported only when the
                very short-term wind speed exceeds the reported
                2-minute wind speed by more than 10 knots
                (11mph or 18kph).
                The “very short-term” period is typically defined
                as about 20 seconds.
                So, if there is a 20 second period where the wind
                is blowing more than 10 knots above the normally
                reported wind speed, this short-term wind speed
                is reported as a gust.
            visibility :
                Describes the horizontal opacity of the atmosphere.
                That is, if you are looking out at other points on the Earth,
                the visibility measure tells you how far away objects can
                be and still be identifiable.
            cloud_cover : How much of the sky is blocked by clouds at a
                          given time from a given location.
            relative_humidity : Amount of water vapor in air relative
                                to total possible.
            weather_type : Text describing significant weather conditions
                           if any. Usually empty.
            sea_level_pressure : Atmospheric pressure adjusted
                                 for height above sea
            dew_point : The temperature the air needs to be cooled to
                        (at constant pressure) in order to achieve a
                        relative humidity (RH) of 100%.
            solar_radiation : The power (in W/m2) at the instantaneous
                              moment of the observation.
            conditions :
                Text describing weather conditions.
                (List of possible options:
                 https://github.com/visualcrossing/WeatherApi/tree/master/lang)
            date  : Datetime of the weather measuring time.
            location : Latitude, longitude of the measurement.
            index : Index of the Weather measurement (0, 1, 2).
        """
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
