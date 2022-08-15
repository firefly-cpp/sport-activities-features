import math
from .classes import StoredSegments
from typing import List
from enum import Enum
import numpy


class GradeUnit(Enum):
    """
    Enum for selecting the type of data we want returned in hill slope calculation (degrees / radians or gradient (%))
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
    def __init__(self, altitudes: List[float], distances: List[float] = None, ascent_threshold: float = 30) -> None:
        """
        Initialisation method of HillIdentification class.\n
        Args:
            altitudes (list):
                an array of altitude values extracted from TCX file
            ascent_threshold (float):
                parameter that defines the hill (hill >= ascent_threshold)
        """
        self.altitudes:List[float] = altitudes
        self.distances:List[float] = distances
        self.ascent_threshold:float = ascent_threshold
        self.identified_hills:List[StoredSegments] = []
        self.total_ascent:float = 0
        self.total_descent:float = 0

    def return_hill(self, ascent:float, ascent_threshold: float = 30) -> bool:
        """
        Method for identifying whether the hill is steep enough to be identified as a hill.\n
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
            differences.append(self.altitudes[i] - self.altitudes[i - 1])
        self.total_ascent = sum(x for x in differences if x > 0)
        self.total_descent = sum(-x for x in differences if x < 0)

        hill_segment = []
        hill_segment_ascent = 0.0

        for i in range(len(differences)):
            total_ascent = 0.0
            selected_IDs = []
            selected_IDs.append(i)
            descent_counter = 0

            for j in range(i + 1, len(differences)):
                NEXT = differences[j]
                if NEXT >= 0.0:
                    total_ascent = total_ascent + NEXT
                    selected_IDs.append(j)

                else:
                    if len(selected_IDs) == 1:
                        break
                    else:
                        selected_IDs.append(j)
                        descent_counter = descent_counter + 1

                if descent_counter == 10:
                    selected_IDs = selected_IDs[
                        : len(selected_IDs) - descent_counter
                    ]
                    break

            if self.return_hill(total_ascent):
                if len(hill_segment) < 3: #Nothing happens...
                    hill_segment = selected_IDs
                    hill_segment_ascent = total_ascent
                else:
                    length_of_intersection = len(
                        set(hill_segment).intersection(selected_IDs)
                    )
                    calculation = float(
                        float(length_of_intersection)
                        / float(len(hill_segment))
                    )
                    if calculation < 0.1: #if less than 10% of nodes repeatž

                        avg_grade = None

                        is_a_list = isinstance(self.distances, numpy.ndarray) or isinstance(self.distances, list)
                        hill_segment_grade = None
                        if is_a_list and len(self.distances) == len(self.altitudes):
                            end_distance = self.distances[hill_segment[-1]]
                            start_distance = self.distances[hill_segment[0]]
                            hill_segment_distance = end_distance - start_distance
                            hill_segment_grade = self.__calculate_hill_grade(hill_segment_distance, hill_segment_ascent)


                        self.identified_hills.append(
                            StoredSegments(hill_segment, hill_segment_ascent, hill_segment_grade)
                        )
                        hill_segment = []
                        hill_segment_ascent = 0.0

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


    def __calculate_hill_grade(self, distance: float, ascent: float, unit:GradeUnit = GradeUnit.DEGREES) -> float:
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
            return ascent/distance
        else:
            raise Exception("Invalid GradeUnit")