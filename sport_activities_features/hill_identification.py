from .classes import StoredSegments


class HillIdentification(object):
    """
    Class for identification of hills from TCX file.\n
    Args:
        altitudes (list):
            an array of altitude values extracted from TCX file
        ascent_threshold (float):
            parameter that defines the hill (hill >= ascent_threshold)
    """
    def __init__(self, altitudes: list, ascent_threshold: float) -> None:
        """
        Initialisation method of HillIdentification class.\n
        Args:
            altitudes (list):
                an array of altitude values extracted from TCX file
            ascent_threshold (float):
                parameter that defines the hill (hill >= ascent_threshold)
        """
        self.altitudes = altitudes
        self.ascent_threshold = ascent_threshold
        self.identified_hills = []
        self.total_ascent = 0
        self.total_descent = 0

    def return_hill(self, ascent_threshold: float) -> bool:
        """
        Method for identifying whether the hill is
        steep enough to be identified as a hill.\n
        Args:
            ascent_threshold (float):
                threshold of the ascent that is used for identifying hills
        Returns:
            bool: True if the hill is recognised, False otherwise
        """
        if ascent_threshold >= 30:
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

        BEST_SEGMENT = []
        BEST_SEGMENT_ASCENT = 0.0

        for i in range(len(differences)):
            TOTAL_ASCENT = 0.0
            selected_IDs = []
            selected_IDs.append(i)
            descent_counter = 0

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
                    selected_IDs = selected_IDs[
                        : len(selected_IDs) - descent_counter
                    ]
                    break

            if self.return_hill(TOTAL_ASCENT):
                if len(BEST_SEGMENT) < 3:
                    BEST_SEGMENT = selected_IDs
                    BEST_SEGMENT_ASCENT = TOTAL_ASCENT
                else:
                    length_of_intersection = len(
                        set(BEST_SEGMENT).intersection(selected_IDs)
                    )
                    calculation = float(
                        float(length_of_intersection)
                        / float(len(BEST_SEGMENT))
                    )
                    if calculation < 0.1:
                        self.identified_hills.append(
                            StoredSegments(BEST_SEGMENT, BEST_SEGMENT_ASCENT)
                        )
                        BEST_SEGMENT = []
                        BEST_SEGMENT_ASCENT = 0.0

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
