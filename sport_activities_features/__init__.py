from sport_activities_features.classes import StoredSegments
from sport_activities_features.data_analysis import DataAnalysis
from sport_activities_features.data_extraction import DataExtraction
from sport_activities_features.data_extraction_from_csv import (
    DataExtractionFromCSV
)
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.interval_identification import (
    IntervalIdentificationByPower,
)
from sport_activities_features.plot_data import PlotData
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures
from sport_activities_features.training_loads import (
    BanisterTRIMP,
    EdwardsTRIMP,
    LuciaTRIMP
)
from sport_activities_features.weather_identification import (
    WeatherIdentification,
)
from sport_activities_features.weather_objects.AverageWeather import (
    AverageWeather
)
from sport_activities_features.weather_objects.Weather import Weather
from sport_activities_features.missing_elevation_identification import (
    ElevationIdentification
)
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.interruptions.interruption_processor import (
    InterruptionProcessor
)


__all__ = [
    'StoredSegments',
    'DataAnalysis',
    'DataExtraction',
    'DataExtractionFromCSV',
    'HillIdentification',
    'IntervalIdentificationByHeartRate',
    'IntervalIdentificationByPower',
    'PlotData',
    'TCXFile',
    'GPXFile',
    'TopographicFeatures',
    'BanisterTRIMP',
    'EdwardsTRIMP',
    'LuciaTRIMP',
    'Weather',
    'WeatherIdentification',
    'AverageWeather',
    'ElevationIdentification',
    'InterruptionProcessor'
]

__version__ = '0.3.2'
