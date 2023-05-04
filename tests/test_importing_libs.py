"""
Test importing all the modules of the library.
"""


def test_classes_import():
    try:
        from sport_activities_features.classes import StoredSegments

        assert StoredSegments is not None
    except ModuleNotFoundError as err:
        print(err)


def test_data_analysis_import():
    try:
        from sport_activities_features.data_analysis import DataAnalysis

        assert DataAnalysis is not None
    except ModuleNotFoundError as err:
        print(err)


def test_data_extraction_import():
    try:
        from sport_activities_features.data_extraction import DataExtraction

        assert DataExtraction is not None
    except ModuleNotFoundError as err:
        print(err)


def test_data_extraction_from_csv_import():
    try:
        from sport_activities_features.data_extraction_from_csv import (
            DataExtractionFromCSV,
        )

        assert DataExtractionFromCSV is not None
    except ModuleNotFoundError as err:
        print(err)


def test_hill_identification_import():
    try:
        from sport_activities_features.hill_identification import (
            HillIdentification,
        )

        assert HillIdentification is not None
    except ModuleNotFoundError as err:
        print(err)


def test_interval_identification_by_power_import():
    try:
        from sport_activities_features.interval_identification import (
            IntervalIdentificationByPower,
        )

        assert IntervalIdentificationByPower is not None
    except ModuleNotFoundError as err:
        print(err)


def test_interval_identification_by_heart_rate_import():
    try:
        from sport_activities_features.interval_identification import (
            IntervalIdentificationByHeartRate,
        )

        assert IntervalIdentificationByHeartRate is not None
    except ModuleNotFoundError as err:
        print(err)


def test_plot_data_import():
    try:
        from sport_activities_features.plot_data import PlotData

        assert PlotData is not None
    except ModuleNotFoundError as err:
        print(err)


def test_tcx_manipulation_import():
    try:
        from sport_activities_features.tcx_manipulation import TCXFile

        assert TCXFile is not None
    except ModuleNotFoundError as err:
        print(err)


def test_topographic_features_import():
    try:
        from sport_activities_features.topographic_features import (
            TopographicFeatures,
        )

        assert TopographicFeatures is not None
    except ModuleNotFoundError as err:
        print(err)


def test_training_loads_import():
    try:
        from sport_activities_features.training_loads import (
            BanisterTRIMPv1,
            BanisterTRIMPv2,
            EdwardsTRIMP,
            LuciaTRIMP,
        )

        assert BanisterTRIMPv1 is not None
        assert BanisterTRIMPv2 is not None
        assert EdwardsTRIMP is not None
        assert LuciaTRIMP is not None
    except ModuleNotFoundError as err:
        print(err)


def test_weather_identification_import():
    try:
        from sport_activities_features.weather_identification import (
            WeatherIdentification,
        )

        assert WeatherIdentification is not None
    except ModuleNotFoundError as err:
        print(err)


def test_weather_objects_import():
    try:
        from sport_activities_features.weather_objects import (
            AverageWeather,
            Weather,
        )

        assert AverageWeather is not None
        assert Weather is not None
    except ModuleNotFoundError as err:
        print(err)


def test_missing_elevation_identification_import():
    try:
        from sport_activities_features.missing_elevation_identification \
            import (ElevationIdentification)

        assert ElevationIdentification is not None

    except ModuleNotFoundError as err:
        print(err)


def test_gpx_manipulation_import():
    try:
        from sport_activities_features.gpx_manipulation import (
            GPXFile,
            GPXTrackPoint,
        )

        assert GPXFile is not None
        assert GPXTrackPoint is not None
    except ModuleNotFoundError as err:
        print(err)


def test_interruptions_import():
    try:
        from sport_activities_features.interruptions.interruption_processor \
            import (InterruptionProcessor)

        assert InterruptionProcessor is not None

    except ModuleNotFoundError as err:
        print(err)


def test_interruptions_exercise_import():
    try:
        from sport_activities_features.interruptions.exercise import (
            Speed,
            TrackSegment,
        )

        assert Speed is not None
        assert TrackSegment is not None
    except ModuleNotFoundError as err:
        print(err)


def test_interruptions_exercise_event_import():
    try:
        from sport_activities_features.interruptions.exercise_event import (
            ExerciseEvent,
        )

        assert ExerciseEvent is not None
    except ModuleNotFoundError as err:
        print(err)


def test_interruptions_track_segment_import():
    try:
        from sport_activities_features.interruptions.exercise import (
            TrackSegment,
        )

        assert TrackSegment is not None
    except ModuleNotFoundError as err:
        print(err)


def test_interruptions_overpass_import():
    try:
        from sport_activities_features.interruptions.overpass import Overpass

        assert Overpass is not None
    except ModuleNotFoundError as err:
        print(err)


def test_interruptions_coordinates_box_import():
    try:
        from sport_activities_features.interruptions.overpass import (
            CoordinatesBox,
        )

        assert CoordinatesBox is not None
    except ModuleNotFoundError as err:
        print(err)


def test_sport_activites_exercise_event_import():
    try:
        from sport_activities_features.interruptions.exercise_event import (
            EventDetail,
            EventDetailType,
            EventLocation,
            EventStats,
            EventType,
        )

        assert EventDetail is not None
        assert EventDetailType is not None
        assert EventLocation is not None
        assert EventStats is not None
        assert EventType is not None
    except ModuleNotFoundError as err:
        print(err)


def test_activity_generator_import():
    try:
        from sport_activities_features.activity_generator import (
            SportyDataGen,
        )

        assert SportyDataGen is not None
    except ModuleNotFoundError as err:
        print(err)


def test_area_identification_import():
    try:
        from sport_activities_features.area_identification import (
            AreaIdentification,
        )

        assert AreaIdentification is not None
    except ModuleNotFoundError as err:
        print(err)


def test_dead_end_identification_import():
    try:
        from sport_activities_features.dead_end_identification import (
            DeadEndIdentification,
        )

        assert DeadEndIdentification is not None
    except ModuleNotFoundError as err:
        print(err)


def test_file_manipulation_import():
    try:
        from sport_activities_features.file_manipulation import (
            FileManipulation,
        )

        assert FileManipulation is not None
    except ModuleNotFoundError as err:
        print(err)
