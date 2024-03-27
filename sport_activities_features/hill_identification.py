import math
from .classes import StoredSegments
from typing import List
from enum import Enum
import numpy


class GradeUnit(Enum):
    """
    Enum for selecting the type of data we want returned in
    hill slope calculation (degrees / radians or gradient (%))
    """

    DEGREES = 1
    RADIANS = 2
    PERCENTS = 3


class HillIdentification(object):
    """
    Class for identification of hills from TCX file.\n
    Args:
        altitudes (list):
            an array of altitude values extracted from TCX file
        ascent_threshold (float):
            parameter that defines the hill (hill >= ascent_threshold)
        distances (list):
            optional, allows calculation of hill grades (steepnes)
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
            ascent_threshold (float):
                parameter that defines the hill (hill >= ascent_threshold)
        """
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
        if ascent >= ascent_threshold:
            return True
        else:
            return False

    def identify_hills(self) -> None:
        """
        Method for identifying hills and extracting
        total ascent and descent from data.\n
        Note:
            [WIP]
            Algorithm is still in its preliminary stage.
        """
        differences = []
        for i in range(1, len(self.altitudes)):
            if (
                type(self.altitudes[i]) is not float
                and type(self.altitudes[i]) is float
            ):
                continue
            differences.append(self.altitudes[i] - self.altitudes[i - 1])
        self.total_ascent = sum(x for x in differences if x > 0)
        self.total_descent = sum(-x for x in differences if x < 0)

        is_ascent = False
        is_descent = False

        ascentX_start = 0

        array_of_changes_indexes = []

        for i in range(1, len(self.altitudes)):
            if self.altitudes[i] >= self.altitudes[i - 1]:
                if not is_descent and not is_ascent:
                    is_ascent = True
                    ascentX_start = i - 1
                elif is_descent:
                    ascent_height = self.altitudes[i-1] - self.altitudes[ascentX_start]
                    array_of_changes_indexes.append([ascentX_start, i-1, ascent_height])

                    ascentX_start = i - 1
                    is_ascent = True
                    is_descent = False

            else:
                if not is_ascent and not is_descent:
                    is_descent = True
                    ascentX_start = i - 1
                elif is_ascent:
                    descent_height = self.altitudes[i-1] - self.altitudes[ascentX_start]
                    array_of_changes_indexes.append([ascentX_start, i-1, descent_height])

                    ascentX_start = i - 1
                    is_descent = True
                    is_ascent = False

        if is_ascent or is_descent:
            height_change = self.altitudes[-1] - self.altitudes[ascentX_start]
            array_of_changes_indexes.append([ascentX_start, len(self.altitudes) - 1, height_change])

        is_ascent = False
        is_descent = False

        current_ascent = 0
        current_descent = 0

        starting_index = 0
        start_x = 0

        if array_of_changes_indexes[0][2] < 0:
            hill_segment_grade = None

            is_a_list = isinstance(
                self.distances, numpy.ndarray
            ) or isinstance(self.distances, list)

            if is_a_list and len(self.distances) == len(
                    self.altitudes
            ):

                end_distance = self.distances[array_of_changes_indexes[0][1]]
                start_distance = self.distances[array_of_changes_indexes[0][0]]
                hill_segment_distance = (
                        end_distance - start_distance
                )
                hill_segment_grade = self.__calculate_hill_grade(
                    hill_segment_distance, abs(array_of_changes_indexes[0][2])
                )

            self.identified_hills.append(
                StoredSegments(
                    [array_of_changes_indexes[0][0], array_of_changes_indexes[0][1]],
                    array_of_changes_indexes[0][2],
                    hill_segment_grade,
                )
            )
            starting_index = starting_index + 1
            start_x = array_of_changes_indexes[0][1]

        for i in range(starting_index, len(array_of_changes_indexes)):

            if array_of_changes_indexes[i][2] > 0:
                current_ascent = current_ascent + array_of_changes_indexes[i][2]
                if current_ascent >= self.ascent_threshold:
                    is_ascent = True
            else:
                current_descent = current_descent + array_of_changes_indexes[i][2]
                if abs(current_descent) >= self.ascent_threshold:
                    is_descent = True

            if (((is_ascent and is_descent) and array_of_changes_indexes[i][2] < 0)
                    or i == (len(array_of_changes_indexes) - 1)):
                hill_segment_grade = None

                is_a_list = isinstance(
                    self.distances, numpy.ndarray
                ) or isinstance(self.distances, list)

                if is_a_list and len(self.distances) == len(
                        self.altitudes
                ):
                    end_distance = self.distances[array_of_changes_indexes[i][1]]
                    start_distance = self.distances[start_x]
                    hill_segment_distance = (
                            end_distance - start_distance
                    )
                    hill_segment_grade = self.__calculate_hill_grade(
                        hill_segment_distance, current_ascent
                    )

                self.identified_hills.append(StoredSegments(
                    [start_x, array_of_changes_indexes[i][1]],
                    current_ascent,
                    hill_segment_grade,
                ))

                start_x = array_of_changes_indexes[i][1]
                is_ascent = False
                is_descent = False
                current_ascent = 0
                current_descent = 0

    def return_hills(self) -> list:
        """
        Method for returning identified hills.\n
        Returns:
            list: array of identified hills
        """
        hills = []
        for i in range(len(self.identified_hills)):
            hills.append(self.identified_hills[i].segment)
        return hills

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
            raise Exception("Invalid GradeUnit")
