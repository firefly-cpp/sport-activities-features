import math

import geotiler
import matplotlib.pyplot as plt
import numpy as np


class AreaIdentification:

    """Area identification based by coordinates.\n
    Args:
        positions (np.array):
            coordinates of positions as an array of latitudes and longitudes
        distances (np.array):
            cummulative distances as an array of floats
        timestamps (np.array):
            information about time as an array of datetimes
        heart_rates (np.array):
            heart rates as an array of integers
        area_coordinates (np.array):
            coordinates of the area where data is analysed as
            an array of latitudes and longitudes
    Reference:
        L. Lukač,
        "Extraction and Analysis of Sport Activity Data Inside Certain Area",
        7th Student Computer Science Research Conference StuCoSReC,
        2021, pp. 47-50,
        doi: https://doi.org/10.18690/978-961-286-516-0.9.
    """

    def __init__(
        self,
        positions: np.array,
        distances: np.array,
        timestamps: np.array,
        heart_rates: np.array,
        area_coordinates: np.array,
    ) -> None:
        """Initialisation method for AreaIdentification class.\n
        Args:
            positions (np.array):
                coordinates of positions as an array of latitudes
                and longitudes
            distances (np.array):
                cummulative distances as an array of floats
            timestamps (np.array):
                information about time as an array of datetimes
            heart_rates (np.array):
                heart rates as an array of integers
            area_coordinates (np.array):
                coordinates of the area where data is analysed as
                an array of latitudes and longitudes.
        """
        self.positions = positions
        self.distances = distances
        self.timestamps = timestamps
        self.heart_rates = heart_rates
        self.area_coordinates = area_coordinates

    def is_equal(self, value_1: float, value_2: float) -> bool:
        """Method for checking whether the two float values are equal
        with certain tolerance (because of round error).\n
        Args:
            value_1 (float):
                first value
            value_2 (float):
                second value
        Returns:
            bool:
                True if the two values are equal, false otherwise.
        """
        tolerance = 0.00001
        # If the absolute value of substraction is smaller than
        # the tolerance threshold, the two values are counted as equal.
        if abs(value_1 - value_2) < tolerance:
            return True
        return False

    def do_two_line_segments_intersect(
        self,
        p1: np.array,
        p2: np.array,
        p3: np.array,
        p4: np.array,
    ) -> bool:
        """Method for checking whether two line segments have
        an intersection point.\n
        Args:
            p1 (np.array):
                first point of the first line as a pair of coordinates
            p2 (np.array):
                second point of the first line as a pair of coordinates
            p3 (np.array):
                first point of the second line as a pair of coordinates
            p4 (np.array):
                second point of the second line as a pair of coordinates
        Returns:
            bool:
                True if the two lines have an intersection point,
                False otherwise.
        """
        # Initialization of vectors and values.
        v12 = np.array(p2 - p1)
        v34 = np.array(p4 - p3)
        v31 = np.array(p1 - p3)
        D = np.cross(v12, v34)
        A = np.cross(v34, v31)
        B = np.cross(v12, v31)

        # If D == 0, the two line segments are parallel
        if self.is_equal(D, 0):
            return False

        Ua = A / D
        Ub = B / D

        # If the intersection point is in the middle of the line
        # segment, the intersection is counted.
        if Ua > 0 and Ua < 1 and Ub > 0 and Ub < 1:
            return True

        return False

    def identify_points_in_area(self) -> None:
        """Method for identifying the measure points of the
        activity inside of the specified area.
        """
        self.points_in_area = np.array([])
        self.points_outside_area = np.array([])
        currently_in_area = False
        p1 = None

        # Checking whether coordinates are inside of the given area.
        for i in np.arange(np.shape(self.positions)[0]):
            number_of_intersections = 0

            # If the ray intersects with the area even times,
            # the point is not inside of the area.
            for border in np.arange(np.shape(self.area_coordinates)[0]):
                for j in np.arange(
                    -1,
                    np.shape(self.area_coordinates[border])[0] - 1,
                ):
                    if self.do_two_line_segments_intersect(
                        self.area_coordinates[border][j],
                        self.area_coordinates[border][j + 1],
                        np.array([self.positions[i][0], self.positions[i][1]]),
                        np.array([190, self.positions[i][1]]),
                    ):
                        number_of_intersections += 1

            # If the number of intersections is odd,
            # the point is inside of the given area.
            if number_of_intersections % 2 == 1:
                if not currently_in_area:
                    p1 = int(i)
                    currently_in_area = True
            else:
                if currently_in_area:
                    self.points_in_area = np.append(
                        self.points_in_area,
                        (p1, int(i) - 1),
                    )
                    p1 = None
                    currently_in_area = False

        self.points_in_area = self.points_in_area.astype('int32')
        self.points_in_area = np.reshape(self.points_in_area, (-1, 2))

    def extract_data_in_area(self) -> dict:
        """Method for extracting the data of the identified points in area.\n
        Returns: area_data: {
                    'distance': distance,
                    'time': time,
                    'average_speed': average_speed,
                    'minimum_heart_rate': minimum_heart_rate,
                    'maximum_heart_rate': maximum_heart_rate,
                    'average_heart_rate': average_heart_rate
                }.
        """
        distance = 0.0
        time = 0.0
        heart_rates = np.array([])

        # Extracting the data from the identified points.
        for i in self.points_in_area:
            try:
                current_distance = self.distances[i][1] - self.distances[i][0]
                current_time = (
                    self.timestamps[i][1]
                    - self.timestamps[i][0]
                ).seconds
                distance += current_distance
                time += current_time

                # Since some of heart rate data may be missing,
                # only existing data are added to the array.
                heart_rates_with_NaN = self.heart_rates[
                    i[0]:i[1]
                ].astype(float)
                not_NaN_values = ~np.isnan(heart_rates_with_NaN)
                heart_rates = np.append(
                    heart_rates,
                    heart_rates_with_NaN[not_NaN_values],
                )
            except Exception:
                pass

        try:
            average_speed = distance / time
        except Exception:
            average_speed = 0.0

        try:
            minimum_heart_rate = np.min(heart_rates)
            maximum_heart_rate = np.max(heart_rates)
            average_heart_rate = np.sum(heart_rates) / np.size(heart_rates)
        except Exception:
            minimum_heart_rate = None
            maximum_heart_rate = None
            average_heart_rate = None

        area_data = {
            'distance': distance,
            'time': time,
            'average_speed': average_speed,
            'minimum_heart_rate': minimum_heart_rate,
            'maximum_heart_rate': maximum_heart_rate,
            'average_heart_rate': average_heart_rate,
        }
        return area_data

    def plot_map(self) -> None:
        """Method for plotting the map using Geotiler
        according to the object variables.
        """
        if np.shape(self.positions)[0] == 0:
            msg = 'Dataset is empty or invalid.'
            raise Exception(msg)

        # Downloading the map.
        size = 10000
        coordinates = self.positions.flatten()
        latitudes = coordinates[::2]
        longitudes = coordinates[1::2]
        map = geotiler.Map(
            extent=(np.min(longitudes),
                    np.min(latitudes),
                    np.max(longitudes),
                    np.max(latitudes),
                    ),
            size=(size, size),
        )
        image = geotiler.render_map(map)

        # Drawing the map as plot.
        ax = plt.subplot(111)
        ax.imshow(image)

        # If there are some points inside of the given area,
        # the segments outside and inside of the area are plotted
        # on the map.
        if np.shape(self.points_in_area)[0] > 0:
            # Drawing the starting path outside of the area.
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1])
                         for p in np.arange(0, self.points_in_area[0][0] + 1)))
            ax.plot(x, y, c='blue', label='Outside of the area')

            # Drawing the path inside of the area and possible paths
            # in between outside of the area.
            for i in np.arange(np.shape(self.points_in_area)[0]):
                x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in
                             np.arange(
                                 self.points_in_area[i][0],
                                 self.points_in_area[i][1] + 1)),
                           )

                if i == 0:
                    ax.plot(
                        x,
                        y,
                        c='red',
                        label='Part of exercise inside of the area',
                    )
                else:
                    ax.plot(
                        x,
                        y,
                        c='red',
                        label='_nolegend_',
                    )

                if np.shape(self.points_in_area)[0] > i + 1:
                    x, y = zip(*(map.rev_geocode(self.positions[p][::-1])
                                 for p in np.arange(
                                    self.points_in_area[i][1],
                                    self.points_in_area[i + 1][0] + 1)
                                 ),
                               )
                    ax.plot(x, y, c='blue', label='_nolegend_')

            # Drawing the ending path outside of the area.
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in
                         np.arange(
                             self.points_in_area[-1][1],
                             np.shape(self.positions)[0],
                         )),
                       )
            ax.plot(x, y, c='blue', label='_nolegend_')
        # If there are no points inside of the given area,
        # the whole path is plotted as outside of the given area.
        else:
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1])
                         for p in np.arange(np.shape(self.positions)[0])),
                       )
            ax.plot(
                x,
                y,
                c='blue',
                label='Part of exercise outside of the area',
            )

        # Drawing the bounding box of the chosen area.
        for hull in self.area_coordinates:
            x, y = zip(*(map.rev_geocode(hull[i - 1][::-1])
                         for i in np.arange(np.shape(hull)[0] + 1)),
                       )
            ax.plot(x, y, c='black', label='Area border')

        ax.legend()
        plt.axis('off')
        plt.xlim((0, size))
        plt.ylim((size, 0))

    def draw_map(self) -> None:
        """Method for the visualization of the exercise on the map using Geotiler."""
        self.plot_map()
        plt.show()

    @staticmethod
    def plot_activities_inside_area_on_map(
        activities: np.array,
        area_coordinates: np.array,
    ) -> None:
        """Static method for plotting the area borders and the activities
        (or their parts) inside of an area.\n
        Args:
            activities (np.array):
                array of AreaIdentification objects
            area_coordinates (np.array):
                border coordinates of an area as an array
                of latitudes and longitudes.
        """
        size = 10000
        coordinates = area_coordinates.flatten()
        latitudes = coordinates[::2]
        longitudes = coordinates[1::2]
        map = geotiler.Map(
            extent=(
                np.min(longitudes),
                np.min(latitudes),
                np.max(longitudes),
                np.max(latitudes),
            ),
            size=(size, size),
        )
        image = geotiler.render_map(map)
        colors = [
            'red',
            'blue',
            'green',
            'cyan',
            'magenta',
            'yellow',
            'key',
            'white',
        ]

        # Drawing the map as plot.
        ax = plt.subplot(111)
        ax.imshow(image)
        for i in np.arange(np.shape(activities)[0]):
            sectors = np.array([])
            for j in np.arange(np.shape(activities[i].points_in_area)[0]):
                sectors = np.append(
                    sectors,
                    zip(*(map.rev_geocode(activities[i].positions[p][::-1])
                          for p in np.arange(
                              activities[i].points_in_area[j][0],
                              activities[i].points_in_area[j][1] + 1)
                          ),
                        ),
                )

            # Plotting each activity (displayed only once in legend).
            for j in np.arange(np.shape(sectors)[0]):
                x, y = sectors[j]
                if j == 0:
                    ax.plot(
                        x,
                        y,
                        c=colors[i % 8],
                        label=f'Activity {i + 1}',
                    )
                else:
                    ax.plot(x, y, c=colors[i % 8], label='_nolegend_')

        # Drawing the bounding box of the chosen area.
        for hull in area_coordinates:
            x, y = zip(*(map.rev_geocode(hull[i - 1][::-1])
                         for i in np.arange(np.shape(hull)[0] + 1)),
                       )
            ax.plot(x, y, c='black', label='Area border')

        ax.legend()
        plt.axis('off')
        plt.xlim((0, size))
        plt.ylim((size, 0))

    @staticmethod
    def draw_activities_inside_area_on_map(
        activities: np.array,
        area_coordinates: np.array,
    ) -> None:
        """Static method for drawing all the activities
        inside of an area on the map.\n
        Args:
            activities (np.array):
                array of AreaIdentification objects
            area_coordinates (np.array):
                border coordinates of an area as an array
                of latitudes and longitudes.
        """
        AreaIdentification.plot_activities_inside_area_on_map(
            activities,
            area_coordinates,
        )
        plt.show()

    @staticmethod
    def get_area_coordinates_around_point(
        point: np.array,
        distance: int,
    ) -> np.array:
        """Static method to get area coordinates around the point on Earth
        according to given distance. Area limits consist of 4 border points.\n
        Args:
            point (np.array):
                a pair of Earth coordinates
            distance (int):
                desired distance from given point to
                area border points
        Returns:
            np.array:
                an array of area coordinates.
        """
        coordinates = np.empty((1, 4, 2))
        lat, lon = point[0], point[1]
        R = 6378137  # Earth's radius (sphere approximation)

        diff_lat = distance / R
        diff_lon = distance / (R * math.cos(math.pi * lat / 180))

        x = lat - diff_lat * 180 / math.pi
        y = lon - diff_lon * 180 / math.pi
        coordinates[0][0] = np.array([x, y])
        x = lat - diff_lat * 180 / math.pi
        y = lon + diff_lon * 180 / math.pi
        coordinates[0][1] = np.array([x, y])
        x = lat + diff_lat * 180 / math.pi
        y = lon + diff_lon * 180 / math.pi
        coordinates[0][2] = np.array([x, y])
        x = lat + diff_lat * 180 / math.pi
        y = lon - diff_lon * 180 / math.pi
        coordinates[0][3] = np.array([x, y])

        return coordinates
