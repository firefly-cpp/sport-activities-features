import geopy.distance


class TopographicFeatures:

    """Class for feature extraction from topographic maps.\n
    Args:
        identified_hills (list):
            identified hills are now passed to this class.
    """

    def __init__(self, identified_hills: list) -> None:
        """Initialisation method of TopographicFeatures class.\n
        Args:
            identified_hills (list):
                identified hills are now passed to this class.
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

    def avg_altitude_of_hills(self, alts: list) -> float:
        """Method for calculating the average altitude of
        all identified hills in sport activity.\n
        Args:
            alts (list):
                list of altitudes
        Returns:
            float: average altitude.
        """
        all_values = []
        for i in range(len(self.identified_hills)):
            alt_points = []
            detected = self.identified_hills[i]
            for j in range(len(detected)):
                alt_points.append(alts[detected[j]])
            all_values.append(sum(alt_points) / float(len(alt_points)))
        if len(all_values) == 0:
            return 0
        else:
            return sum(all_values) / float(len(all_values))

    def distance_of_hills(self, positions: list) -> float:
        """Method for calculating the total distance of all
        identified hills in sport activity.\n
        Args:
            positions (list):
                list of positions
        Returns:
            float: distance of hills.
        """
        total_distance = 0.0
        for i in range(len(self.identified_hills)):
            current = self.identified_hills[i]

            index_range = []

            start = current[0] + 1
            if current[0] == 0:
                start = 0

            for index in range(start, current[1]):
                index_range.append(index)

            distance = 0.0
            if len(positions) < 5:
                total_distance = 0.0
            else:
                for _j in range(len(index_range) - 1):
                    distance = distance + self.calculate_distance(
                        positions[i][0],
                        positions[i + 1][0],
                        positions[i][1],
                        positions[i + 1][1],
                    )

            total_distance = total_distance + distance

        return total_distance

    def share_of_hills(self, hills_dist: float, total_dist: float) -> float:
        """Method for calculating the share of hills
        in sport activity (percentage).\n
        Args:
            hills_dict (float):
                distance of all hills
            total_dist (float):
                total distance
        Returns:
            float: share of hills.
        """
        if total_dist == 0:
            return 0
        else:
            return float(hills_dist / (total_dist / 1000))

    def avg_ascent_of_hills(self, alts: list) -> float:
        """Method for calculating the average ascent
        of all hills in sport activity.\n
        Args:
            alts (list):
                list of altitudes
        Returns:
            float: average ascent.
        """
        all_values = []
        for i in range(len(self.identified_hills)):
            alt_points = []
            detected = self.identified_hills[i]
            for j in range(len(detected)):
                alt_points.append(alts[detected[j]])

            ascent = self.ascent(alt_points)
            all_values.append(ascent)
        if len(all_values) == 0:
            return 0
        else:
            return sum(all_values) / float(len(all_values))

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
