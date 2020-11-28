import os
from .classes import StoredSegments


class HillIdentification(object):
    r"""Identification of Hills from TCX file.

        Attributes:
                altitudes: An array of altitude values extracted from TCX file
                ascent_threshold (float): Parameter that defines the hill (hill >= ascent_threshold)

        """

    def __init__(self, altitudes, ascent_threshold):
        self.altitudes = altitudes
        self.ascent_threshold = ascent_threshold
        self.identified_hills = []

    def return_hill(self, ascent_threshold):
        r"""Return

                Returns:
                        bool:

                """
        if ascent_threshold >= 30:
            return True
        else:
            return False

    def identify_hills(self):
        r"""Algorithm for the identification of hills from data.

                Note:
                        * :Algorithm is still in its preliminary stage.
                """
        differences = []
        for i in range(1, len(self.altitudes)):
            differences.append(self.altitudes[i] - self.altitudes[i - 1])
        
        BEST_SEGMENT = []
        BEST_SEGMENT_ASCENT = 0.0

        for i in range(len(differences)):
            CURRENT = differences[i]
            TOTAL_ASCENT = 0.0
            selected_IDs = []
            selected_IDs.append(i)
            descent_counter = 0

            descent_flag = True
            for j in range(i + 1, len(differences)):
                NEXT = differences[j]
                if NEXT >= 0.0:
                    TOTAL_ASCENT = TOTAL_ASCENT + NEXT
                    selected_IDs.append(j)

                else:
                    if len(selected_IDs) == 1:
                        break
                    else:
                        selected_IDs.append(j)
                        descent_counter = descent_counter + 1

                if descent_counter == 10:
                    selected_IDs = selected_IDs[:len(
                        selected_IDs) - descent_counter]
                    break

            if self.return_hill(TOTAL_ASCENT):
                if len(BEST_SEGMENT) < 3:
                    BEST_SEGMENT = selected_IDs
                    BEST_SEGMENT_ASCENT = TOTAL_ASCENT
                else:
                    length_of_intersection = len(
                        set(BEST_SEGMENT).intersection(selected_IDs))
                    calculation = float(
                        float(length_of_intersection) /
                        float(
                            len(BEST_SEGMENT)))
                    if calculation < 0.1:
                        self.identified_hills.append(
                            StoredSegments(BEST_SEGMENT, BEST_SEGMENT_ASCENT))
                        BEST_SEGMENT = []
                        BEST_SEGMENT_ASCENT = 0.0

    def return_hills(self):
        r"""Return identified hills.

                Returns:
                        str: Array of identified hills.

                """
        hills = []
        for i in range(len(self.identified_hills)):
            hills.append(self.identified_hills[i].segment)
        return hills
