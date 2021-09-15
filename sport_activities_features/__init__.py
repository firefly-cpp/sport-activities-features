from sport_activities_features.classes import StoredSegments
from sport_activities_features.data_analysis import DataAnalysis
from sport_activities_features.data_extraction import DataExtraction
from sport_activities_features.data_extraction_from_csv import DataExtractionFromCSV
from sport_activities_features.hill_identification import HillIdentification
from sport_activities_features.interval_identification import (
    IntervalIdentificationByHeartrate,
    IntervalIdentificationByPower,
)
from sport_activities_features.plot_data import PlotData
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures
from sport_activities_features.training_loads import BanisterTRIMP
from sport_activities_features.weather_identification import (
    Weather,
    WeatherIdentification,
)

__all__ = [
    "StoredSegments",
    "DataAnalysis",
    "DataExtraction",
    "DataExtractionFromCSV",
    "HillIdentification",
    "IntervalIdentificationByHeartrate",
    "IntervalIdentificationByPower",
    "PlotData",
    "TCXFile",
    "TopographicFeatures",
    "BanisterTRIMP",
    "Weather",
    "WeatherIdentification",
]

__version__ = "0.1.1"
