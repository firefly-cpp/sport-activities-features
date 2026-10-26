import geopy.distance


class TopographicFeatures:

    """Class for feature extraction from topographic maps.\n
    Args:
        identified_hills (list):
            list of identified hills.
    """

    def __init__(self, identified_hills: list) -> None:
        """Initialisation method of TopographicFeatures class.\n
        Args:
            identified_hills (list):
                list of identified hills.
        """
        self.identified_hills = identified_hills
        self.features = []

    def num_of_hills(self) -> int:
        """Method for calculating the number of
        identified hills in sport activity.\n
        Returns:
            int: number of hills.
        """
        return len(self.identified_hills)

    @staticmethod
    def _hill_indexes(hill: list) -> range:
        """Return all point indexes of a hill given as [start, end]."""
        return range(hill[0], hill[-1] + 1)

    @staticmethod
    def _valid_altitudes(alts: list, indexes: range) -> list:
        """Return altitudes at the given indexes, skipping missing values."""
        values = []
        for index in indexes:
            altitude = alts[index]
            if altitude is None or altitude != altitude:  # None or NaN
                continue
            values.append(altitude)
        return values

    def avg_altitude_of_hills(self, alts: list) -> float:
        """Method for calculating the average altitude of
        all identified hills in sport activity.\n
        The average altitude of each hill is calculated over all of its
        points; the result is the mean of these values.\n
        Args:
            alts (list):
                list of altitudes
        Returns:
            float: average altitude.
        """
        all_values = []
        for hill in self.identified_hills:
            alt_points = self._valid_altitudes(alts, self._hill_indexes(hill))
            if alt_points:
                all_values.append(sum(alt_points) / len(alt_points))
        if len(all_values) == 0:
            return 0
        return sum(all_values) / len(all_values)

    def distance_of_hills(self, positions: list) -> float:
        """Method for calculating the total distance of all
        identified hills in sport activity.\n
        Args:
            positions (list):
                list of (latitude, longitude) positions
        Returns:
            float: distance of hills in kilometers.
        """
        total_distance = 0.0
        for hill in self.identified_hills:
            indexes = self._hill_indexes(hill)
            for index in indexes[:-1]:
                start = positions[index]
                end = positions[index + 1]
                if (
                    start is None or end is None
                    or None in (start[0], start[1], end[0], end[1])
                ):
                    continue
                total_distance += self.calculate_distance(
                    start[0], end[0], start[1], end[1],
                )
        return total_distance

    def share_of_hills(self, hills_dist: float, total_dist: float) -> float:
        """Method for calculating the share of hills
        in sport activity.\n
        Args:
            hills_dist (float):
                distance of all hills in kilometers
                (see distance_of_hills)
            total_dist (float):
                total distance in meters
        Returns:
            float: share of hills as a ratio between 0 and 1.
        """
        if not total_dist:
            return 0
        return float(hills_dist / (total_dist / 1000))

    def avg_ascent_of_hills(self, alts: list) -> float:
        """Method for calculating the average ascent
        of all hills in sport activity.\n
        The ascent of each hill is the sum of all positive altitude
        changes between its consecutive points.\n
        Args:
            alts (list):
                list of altitudes
        Returns:
            float: average ascent.
        """
        all_values = []
        for hill in self.identified_hills:
            alt_points = self._valid_altitudes(alts, self._hill_indexes(hill))
            all_values.append(self.ascent(alt_points))
        if len(all_values) == 0:
            return 0
        return sum(all_values) / len(all_values)

    def ascent(self, altitude_data: list) -> float:
        """Method for ascent calculation.\n
        Args:
            altitude_data (list):
                list of altitudes
        Returns:
            float: total ascent
        Note:
            [WIP]
            This method should be improved.
        """
        total_ascent = 0.0
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i + 1] - altitude_data[i]
            if diff > 0.0:
                total_ascent += diff
        return total_ascent

    def descent(self, altitude_data: list) -> float:
        """Method for descent calculation.\n
        Args:
            altitude_data (list):
                list of altitudes
        Returns:
            float: total descent
        Note:
            [WIP]
            This method should be improved.
        """
        total_descent = 0.0
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i + 1] - altitude_data[i]
            if diff < 0.0:
                total_descent += abs(diff)
        return total_descent

    def calculate_distance(
        self,
        latitude_1: float,
        latitude_2: float,
        longitude_1: float,
        longitude_2: float,
    ) -> float:
        """Method for calculating the distance between
        the two pairs of coordinates.\n
        Args:
            latitude_1 (float):
                first latitude
            latitude_2 (float):
                second latitude
            longitude_1 (float):
                first longitude
            longitude_2 (float):
                second longitude
        Returns:
            float: distance in kilometers.
        """
        coords_1 = (latitude_1, longitude_1)
        coords_2 = (latitude_2, longitude_2)

        return geopy.distance.geodesic(coords_1, coords_2).km

    def calculate_hill_gradient(
        self,
        latitude_1: float,
        latitude_2: float,
        longitude_1: float,
        longitude_2: float,
        height_1: float,
        height_2: float,
    ) -> float:
        """Method for calculation of the hill gradient in percent.\n
        Args:
            latitude_1 (float):
                first latitude
            latitude_2 (float):
                second latitude
            longitude_1 (float):
                first longitude
            longitude_2 (float):
                second longitude
            height_1 (float):
                first altitude
            height_2 (float):
                second altitude
        Returns:
            float: gradient in degrees.
        """
        # Calculation of distance between given coordinates in meters
        distance = 1000 * self.calculate_distance(
            latitude_1,
            latitude_2,
            longitude_1,
            longitude_2,
        )
        # Calculation of height change in meters
        height_change = height_2 - height_1

        # Calculation of the gradient in percent
        gradient = (100 * height_change / distance)
        return gradient
