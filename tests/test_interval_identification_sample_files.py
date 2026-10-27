"""Interval identification checks on every sample activity in tests/data.

These tests check properties that must hold for any activity instead of
exact values, so they cover new sample files automatically and do not
need updating when the interval rules are tuned.
"""
import glob
import os

import pytest

from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.interval_identification import (
    IntervalIdentificationByHeartRate,
    IntervalIdentificationByPower,
)
from sport_activities_features.tcx_manipulation import TCXFile

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SAMPLE_FILES = sorted(
    glob.glob(os.path.join(DATA_DIR, '*.tcx'))
    + glob.glob(os.path.join(DATA_DIR, '*.gpx')),
)
MASS = 70


def load(path):
    reader = TCXFile() if path.endswith('.tcx') else GPXFile()
    return reader.extract_activity_data(reader.read_one_file(path))


def is_number(value):
    return value is not None and value == value  # not None and not NaN


@pytest.fixture(
    scope='module',
    params=SAMPLE_FILES,
    ids=[os.path.basename(path) for path in SAMPLE_FILES],
)
def activity(request):
    activity = load(request.param)
    if len(activity['timestamps']) < 2:
        pytest.skip('activity has fewer than two points')
    return activity


@pytest.fixture(scope='module')
def by_power(activity):
    intervals = IntervalIdentificationByPower(
        activity['distances'], activity['timestamps'],
        activity['altitudes'], MASS,
    )
    intervals.identify_intervals()
    return intervals


@pytest.fixture(scope='module')
def by_heart_rate(activity):
    intervals = IntervalIdentificationByHeartRate(
        activity['distances'], activity['timestamps'],
        activity['altitudes'], activity['heartrates'],
    )
    try:
        intervals.identify_intervals()
    except ValueError as error:
        # The only accepted failure: heart rate missing for too long.
        assert 'not complete' in str(error)
        pytest.skip(str(error))
    return intervals


def test_sample_files_found():
    assert len(SAMPLE_FILES) >= 10


def check_intervals(intervals, timestamps, above_average):
    """Properties shared by both kinds of intervals."""
    previous_end = -1
    for interval in intervals.return_intervals():
        first, last = interval[0], interval[-1]
        assert previous_end < first <= last, 'ordered, not overlapping'
        assert interval == list(range(first, last + 1)), 'contiguous'
        duration = (timestamps[last] - timestamps[first]).total_seconds()
        assert duration >= intervals.minimum_time, 'long enough'
        assert above_average(first) and above_average(last), (
            'starts and ends above the average'
        )
        previous_end = last

    statistics = intervals.calculate_interval_statistics()
    assert statistics['number_of_intervals'] == len(intervals.intervals)


def test_power_intervals(activity, by_power):
    powers = by_power.powers
    assert len(powers) == len(activity['timestamps']) - 1
    assert all(power >= 0 for power in powers)
    average = sum(powers) / len(powers)
    check_intervals(
        by_power, activity['timestamps'], lambda i: powers[i] > average,
    )


def test_heart_rate_intervals(activity, by_heart_rate):
    heart_rates = activity['heartrates']
    recorded = [hr for hr in heart_rates if is_number(hr)]
    if not recorded:
        assert by_heart_rate.return_intervals() == []
        return
    average = sum(recorded) / len(recorded)
    check_intervals(
        by_heart_rate, activity['timestamps'],
        lambda i: is_number(heart_rates[i]) and heart_rates[i] > average,
    )
