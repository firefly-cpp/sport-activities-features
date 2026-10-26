import math
import warnings
from enum import Enum
from typing import List, Optional

from .classes import StoredSegments

# Points of a climb within this many meters of its lowest altitude are
# treated as flat ground before the climb, so the hill starts at the last
# of them (prevents long flat sections from being counted as part of it).
FLAT_TOLERANCE = 1.0


class GradeUnit(Enum):
    """
    Enum for selecting the type of data we want returned in
    hill slope calculations.\n
     - degrees
     - radians
     - percents [%] (gradient)
    """

    DEGREES = 1
    RADIANS = 2
    PERCENTS = 3


def _is_valid_number(value) -> bool:
    """Return True if value is a real, finite number (not None or NaN)."""
    if value is None or isinstance(value, bool):
        return False
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


class HillIdentification(object):
    """
    Class for identification of hills from TCX file.\n
    A hill is a climb from a low point (valley) to a high point (summit)
    whose elevation gain is at least ``ascent_threshold`` meters. Small
    dips during the climb are tolerated: the climb ends only when the
    altitude drops at least ``ascent_threshold`` meters below the summit
    reached so far (or when the activity ends). Flat ground before the
    climb (within FLAT_TOLERANCE meters of its lowest point) is not part
    of the hill.\n
    Args:
        altitudes (list):
            an array of altitude values extracted from TCX file
        distances (list):
            optional, cumulative distances in meters; allows calculation
            of hill grades (steepness)
        ascent_threshold (float):
            parameter that defines the hill (hill >= ascent_threshold)
    """

    def __init__(
        self,
        altitudes: List[float],
        distances: List[float] = None,
        ascent_threshold: float = 30,
    ) -> None:
        """
        Initialisation method of HillIdentification class.\n
        Args:
            altitudes (list):
                an array of altitude values extracted from TCX file
            distances (list):
                optional, cumulative distances in meters; allows
                calculation of hill grades (steepness)
            ascent_threshold (float):
                parameter that defines the hill (hill >= ascent_threshold)
        """
        if distances is not None and _is_valid_number(distances):
            warnings.warn(
                'HillIdentification received a number as `distances`. '
                'Pass the threshold by keyword: '
                'HillIdentification(altitudes, distances, '
                'ascent_threshold=30). Hill grades will not be calculated.',
                stacklevel=2,
            )
            distances = None

        self.altitudes: List[float] = altitudes
        self.distances: List[float] = distances
        self.ascent_threshold: float = ascent_threshold
        self.identified_hills: List[StoredSegments] = []
        self.total_ascent: float = 0
        self.total_descent: float = 0

    def return_hill(self, ascent: float, ascent_threshold: float = 30) -> bool:
        """
        Method for identifying whether the hill is steep enough
        to be identified as a hill.\n
        Args:
            ascent (float):
                actual ascent of the hill
            ascent_threshold (float):
                threshold of the ascent that is used for identifying hills
        Returns:
            bool: True if the hill is recognised, False otherwise
        """
        return ascent >= ascent_threshold

    def identify_hills(self) -> None:
        """
        Method for identifying hills and extracting
        total ascent and descent from data.\n
        Missing altitude values (None or NaN) are skipped. Calling the
        method again recalculates the results from scratch.
        """
        self.identified_hills = []
        self.total_ascent = 0
        self.total_descent = 0

        valid_indexes = [
            i for i, altitude in enumerate(self.altitudes)
            if _is_valid_number(altitude)
        ]
        if len(valid_indexes) < 2:
            return

        altitudes = self.altitudes

        for previous, current in zip(valid_indexes, valid_indexes[1:]):
            difference = altitudes[current] - altitudes[previous]
            if difference > 0:
                self.total_ascent += difference
            else:
                self.total_descent -= difference

        valley = valid_indexes[0]
        summit = None

        for i in valid_indexes[1:]:
            altitude = altitudes[i]

            if summit is None:
                # Looking for the start of a climb.
                if altitude <= altitudes[valley]:
                    valley = i
                else:
                    summit = i
                continue

            if altitude > altitudes[summit]:
                summit = i
            elif altitudes[summit] - altitude >= self.ascent_threshold:
                # Dropped far enough below the summit: the climb is over.
                self.__store_hill(valley, summit)
                valley = i
                summit = None
            elif altitude <= altitudes[valley]:
                # Fell back below the start before gaining enough height.
                valley = i
                summit = None

        if summit is not None:
            self.__store_hill(valley, summit)

    def __store_hill(self, start: int, end: int) -> None:
        """
        Store the climb from index start to index end if its elevation
        gain reaches the ascent threshold.\n
        Args:
            start (int):
                index of the lowest point of the climb
            end (int):
                index of the highest point of the climb
        """
        lowest = self.altitudes[start]
        for index in range(start + 1, end):
            altitude = self.altitudes[index]
            if (
                _is_valid_number(altitude)
                and altitude <= lowest + FLAT_TOLERANCE
            ):
                start = index

        ascent = self.altitudes[end] - self.altitudes[start]
        if not self.return_hill(ascent, self.ascent_threshold):
            return

        self.identified_hills.append(
            StoredSegments(
                [start, end],
                ascent,
                self.__hill_grade(start, end, ascent),
            ),
        )

    def __hill_grade(
        self, start: int, end: int, ascent: float,
    ) -> Optional[float]:
        """
        Average grade of the climb in degrees, or None if distances
        are not available.\n
        Args:
            start (int):
                index of the lowest point of the climb
            end (int):
                index of the highest point of the climb
            ascent (float):
                elevation gain of the climb in meters
        Returns:
            float: hill grade in degrees, or None
        """
        if self.distances is None:
            return None
        try:
            if len(self.distances) != len(self.altitudes):
                return None
            start_distance = self.distances[start]
            end_distance = self.distances[end]
        except TypeError:
            return None
        if not (
            _is_valid_number(start_distance)
            and _is_valid_number(end_distance)
        ):
            return None

        distance = end_distance - start_distance
        if distance <= 0:
            return None
        return self.__calculate_hill_grade(distance, ascent)

    def return_hills(self) -> list:
        """
        Method for returning identified hills.\n
        Returns:
            list: list of [start_index, end_index] pairs, one for each
            identified hill (from the lowest to the highest point)
        """
        return [hill.segment for hill in self.identified_hills]

    def __calculate_hill_grade(
        self,
        distance: float,
        ascent: float,
        unit: GradeUnit = GradeUnit.DEGREES,
    ) -> float:
        """
        Calculates angle (grade) of the hill from distance and ascent
        Args:
            distance (float):
                distance between points
            ascent (float):
                ascent of the hill in meters
            unit (GradeUnit):
                return type DEGREES or RADIANS or PERCENTS
        Returns:
            float: hill grade (in degrees, radians or percents)
        """
        if unit == GradeUnit.RADIANS:
            return math.atan(ascent / distance)
        elif unit == GradeUnit.DEGREES:
            return math.degrees(math.atan(ascent / distance))
        elif unit == GradeUnit.PERCENTS:
            return ascent / distance
        else:
            raise ValueError('Invalid GradeUnit')
