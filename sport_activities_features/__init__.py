from sport_activities_features.classes import StoredSegments
from sport_activities_features.data_extraction import DataExtraction
from sport_activities_features.data_extraction_from_csv import (
    DataExtractionFromCSV,
)
from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.interruptions.interruption_processor import (
    InterruptionProcessor,
)
from sport_activities_features.interval_identification import (
    IntervalIdentificationByHeartRate,
    IntervalIdentificationByPower,
)
from sport_activities_features.missing_elevation_identification import (
    ElevationIdentification, ElevationApiType
)
from sport_activities_features.plot_data import PlotData
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures
from sport_activities_features.training_loads import (
    BanisterTRIMPv1,
    BanisterTRIMPv2,
    EdwardsTRIMP,
    LuciaTRIMP,
)
from sport_activities_features.weather_identification import (
    WeatherIdentification,
)
from sport_activities_features.weather_objects.AverageWeather import (
    AverageWeather,
)
from sport_activities_features.weather_objects.Weather import Weather

__all__ = [
    'StoredSegments',
    'DataExtraction',
    'DataExtractionFromCSV',
    'HillIdentification',
    'IntervalIdentificationByHeartRate',
    'IntervalIdentificationByPower',
    'PlotData',
    'TCXFile',
    'GPXFile',
    'TopographicFeatures',
    'BanisterTRIMPv1',
    'BanisterTRIMPv2',
    'EdwardsTRIMP',
    'LuciaTRIMP',
    'Weather',
    'WeatherIdentification',
    'AverageWeather',
    'ElevationIdentification',
    'InterruptionProcessor',
    'activity_generator',
    'area_identification',
    'classes',
    'data_analysis',
    'data_extraction',
    'data_extraction_from_csv',
    'dead_end_identification',
    'file_manipulation',
    'gpx_manipulation',
    'hill_identification',
    'interval_identification',
    'missing_elevation_identification',
    'overpy_node_manipulation',
    'plot_data',
    'tcx_manipulation',
    'topographic_features',
    'training_loads',
    'weather_identification',
]

__version__ = '0.4.2'
