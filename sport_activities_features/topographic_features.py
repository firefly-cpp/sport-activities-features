import os
import geopy.distance


class TopographicFeatures(object):
    r"""Implementation of feature extraction from topographic maps.

        Attributes:
                identified_hills: Identified hills are now passed to this class.

        """

    def __init__(self, identified_hills):
        self.identified_hills = identified_hills
        self.features = []

    def num_of_hills(self):
        r"""FEATURE: Number of identified hills in sport activity.

                Returns:
                        int: number of hills

                """
        return len(self.identified_hills)

    def avg_altitude_of_hills(self, alts):
        r"""FEATURE: The average altitude of all identified hills in sport activity.

                Returns:
                        float: average altitude

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

    def distance_of_hills(self, positions):
        r"""FEATURE: Total distance of all identified hills in sport activity.

                Returns:
                        float: distance of hills

                """
        total_distance = 0.0
        for i in range(len(self.identified_hills)):
            current = self.identified_hills[i]
            distance = 0.0
            if(len(positions) < 5):
                total_distance = 0.0
            else:
                for j in range(len(current) - 1):
                    distance = distance + self.calculate_distance(
                        positions[i][0], positions[i + 1][0], positions[i][1], positions[i + 1][1])

            total_distance = total_distance + distance

        return total_distance

    def share_of_hills(self, hills_dist, total_dist):
        r"""FEATURE: Share of hills in sport activity (percentage)

                Returns:
                        float: share of hills

                """
        if total_dist == 0:
            return 0
        else:
            return float(hills_dist / (total_dist / 1000))

    def avg_ascent_of_hills(self, alts):
        r"""FEATURE: Average ascent of all hills in sport activity.

                Returns:
                        float: average ascent

                """
        all_values = []
        for i in range(len(self.identified_hills)):
            ascents = []
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

    def ascent(self, altitude_data):
        r"""Implementation of ascent calculation (should be improved)

                Returns:
                        float: total ascent

                """
        total_ascent = 0.0
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i + 1] - altitude_data[i]
            if diff > 0.0:
                total_ascent += diff
        return total_ascent

    def descent(self, altitude_data):
        r"""Implementation of descent calculation (should be improved)

                Returns:
                        float: total descent

                """
        total_descent = 0.0
        for i in range(len(altitude_data) - 1):
            diff = altitude_data[i + 1] - altitude_data[i]
            if diff < 0.0:
                total_descent += abs(diff)
        return total_descent

    def calculate_distance(self, lat1, lat2, lon1, lon2):
        coords_1 = (lat1, lon1)
        coords_2 = (lat2, lon2)

        return geopy.distance.geodesic(coords_1, coords_2).km
