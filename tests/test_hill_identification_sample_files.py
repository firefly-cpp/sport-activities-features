"""Hill identification checks on every sample activity in tests/data.

These tests check properties that must hold for any activity instead of
exact values, so they cover new sample files automatically and do not
need updating when the hill definition is tuned.
"""
import glob
import os

import pytest

from sport_activities_features.gpx_manipulation import GPXFile
from sport_activities_features.hill_identification import (
    HillIdentification,
)
from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.topographic_features import TopographicFeatures

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
SAMPLE_FILES = sorted(
    glob.glob(os.path.join(DATA_DIR, '*.tcx'))
    + glob.glob(os.path.join(DATA_DIR, '*.gpx')),
)
ASCENT_THRESHOLD = 30

# GPS positions recorded while swimming are too noisy to compare the
# distance along the positions with the distance measured by the device.
NOISY_POSITIONS = {'swimming_activity_1.tcx'}


def load(path):
    reader = TCXFile() if path.endswith('.tcx') else GPXFile()
    exercise = reader.read_one_file(path)
    return exercise, reader.extract_activity_data(exercise)


def has_value(value):
    return value is not None and value == value  # not None and not NaN


@pytest.fixture(
    scope='module',
    params=SAMPLE_FILES,
    ids=[os.path.basename(path) for path in SAMPLE_FILES],
)
def sample(request):
    path = request.param
    exercise, activity = load(path)
    hill = HillIdentification(
        activity['altitudes'],
        activity['distances'],
        ascent_threshold=ASCENT_THRESHOLD,
    )
    hill.identify_hills()
    return {
        'name': os.path.basename(path),
        'exercise': exercise,
        'activity': activity,
        'hill': hill,
        'hills': hill.return_hills(),
    }


def test_sample_files_found():
    assert len(SAMPLE_FILES) >= 10


def test_every_hill_reaches_threshold(sample):
    altitudes = sample['activity']['altitudes']
    for stored in sample['hill'].identified_hills:
        start, end = stored.segment
        assert altitudes[end] - altitudes[start] >= ASCENT_THRESHOLD
        assert stored.ascent == pytest.approx(
            altitudes[end] - altitudes[start],
        )


def test_hills_are_ordered_and_do_not_overlap(sample):
    previous_end = -1
    for start, end in sample['hills']:
        assert previous_end <= start < end
        previous_end = end
    if sample['hills']:
        assert previous_end < len(sample['activity']['altitudes'])


def test_hill_grades_are_positive(sample):
    for stored in sample['hill'].identified_hills:
        if stored.average_slope is not None:
            assert 0 < stored.average_slope < 90


def test_total_ascent_matches_file(sample):
    expected = getattr(sample['exercise'], 'ascent', None)
    if not has_value(expected):
        pytest.skip('file does not provide total ascent')
    assert sample['hill'].total_ascent == pytest.approx(expected, abs=0.5)


def test_distance_of_hills_matches_recorded_distance(sample):
    if sample['name'] in NOISY_POSITIONS:
        pytest.skip('GPS positions are too noisy')

    activity = sample['activity']
    distances = activity['distances']
    hills = sample['hills']
    from_positions = TopographicFeatures(hills).distance_of_hills(
        activity['positions'],
    )
    recorded = sum(distances[end] - distances[start] for start, end in hills)
    assert from_positions == pytest.approx(
        recorded / 1000, rel=0.01, abs=0.05,
    )


def test_activity_without_altitudes_has_no_hills(sample):
    if any(has_value(a) for a in sample['activity']['altitudes']):
        pytest.skip('activity has altitudes')
    assert sample['hills'] == []
    assert sample['hill'].total_ascent == 0
