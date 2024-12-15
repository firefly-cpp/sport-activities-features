from sport_activities_features.interruptions.interruption_processor import (
    InterruptionProcessor,
)
from sport_activities_features.tcx_manipulation import TCXFile

"""
Identify interruption events from a TCX or GPX file.
"""

# read TCX file (also works with GPX files)
tcx_file = TCXFile()
tcx_exercise = tcx_file.read_one_file('path_to_the_data')
tcx_data = tcx_file.extract_activity_data(tcx_exercise)

"""
Time interval = time before and after the start of an event
Min speed = Threshold speed to trigger an event / interruption
            (trigger when under min_speed)
overpass_api_url = Set to something self hosted, or use public instance
                   from https://wiki.openstreetmap.org/wiki/Overpass_API
"""
interruptionProcessor = InterruptionProcessor(
                            time_interval=60,
                            min_speed=2,
                            overpass_api_url='url_to_overpass_api')

"""
If classify is set to true, also discover if interruptions
are close to intersections. Returns a list of [ExerciseEvent]
"""
events = interruptionProcessor.events(tcx_data, True)
