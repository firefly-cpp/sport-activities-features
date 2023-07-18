class StoredSegments:

    """Class for stored segments.\n
    Args:
        segment ():

        ascent ():

        average_slope():

    Note:
    ----
        [WIP]
        This class is still under developement,
        therefore its methods may not work as expected.
    """

    def __init__(self, segment, ascent, average_slope=None) -> None:
        """Initialisation method for StoredSegments class.\n
        Args:
            segment ():

            ascent ():
            average_slope ():
                in degrees

        """
        self.segment = segment
        self.ascent = ascent
        self.average_slope = average_slope
