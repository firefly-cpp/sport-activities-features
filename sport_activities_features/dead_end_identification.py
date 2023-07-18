import math

import geopy.distance
import geotiler
import matplotlib.pyplot as plt
import numpy as np


class DeadEndIdentification:

    """Class for identifying and visualising dead ends in an exercise.
    Dead end is a part of an exercise, where an athlete suddenly makes
    a U-turn takes the same path as before the U-turn is conducted
    in the opposite direction.\n
    Args:
        positions (np.array):
            array of positions as pairs of latitudes and longitudes
        distances (np.array):
            array of cummulative distances
        tolerance_degrees (float):
            tolerance of driving the same route in
            the opposite direction given in degrees
        tolerance_position (float):
            tolerance of positions given in meters
        minimum_distance (int):
            minimum distance of a dead end
        U_turn_allowed_distance (int):
            maximum distance of a U-turn while
            turning around and starting a dead end
    Note:
        [WIP]
        This class is still under developement, therefore
        its methods may not work as expected.
    """

    def __init__(
        self,
        positions: np.array,
        distances: np.array,
        tolerance_degrees: float = 5.0,
        tolerance_position: float = 5.0,
        minimum_distance: int = 500,
        U_turn_allowed_distance: int = 50,
    ) -> None:
        """Initialisation method for DeadEndIdentification class.

        Args:
        ----
            positions (np.array):
                array of positions as pairs of latitudes and longitudes
            distances (np.array):
                array of cummulative distances
            tolerance_degrees (float):
                tolerance of driving the same route in
                the opposite direction given in degrees
            tolerance_position (float):
                tolerance of positions given in meters
            minimum_distance (int):
                minimum distance of a dead end
            U_turn_allowed_distance (int):
                maximum distance of a U-turn while
                turning around and starting a dead end.
        """
        # Reorganizing the exercise data in order to achieve better results.
        self.reorganize_exercise_data(
            np.array(positions),
            np.array(distances),
            interval_distance=1,
        )
        self.tolerance_degrees = tolerance_degrees
        self.tolerance_position = tolerance_position
        self.minimum_distance = minimum_distance
        self.U_turn_allowed_distance = U_turn_allowed_distance

    def reorganize_exercise_data(
        self,
        positions: np.array,
        distances: np.array,
        interval_distance: int = 1,
    ) -> None:
        """Method for reorganising the exercise in the way that the
        trackpoints are organized in a constant interval of distance.\n
        Args:
            positions (np.array):
                array of positions as pairs of latitudes and longitudes
            distances (np.array):
                array of cummulative distances
            interval_distance (int):
                desired distance between two neighboring points.
        """
        distance = distances[-1]
        self.distances = np.arange(math.ceil(distance))
        self.positions = np.empty((0, 2), float)

        j = 0
        for i in np.arange(np.shape(self.distances)[0] - 1):
            while i > distances[j + 1]:
                j += 1

            position1 = positions[j]
            position2 = positions[j + 1]
            distance1 = distances[j]
            distance2 = distances[j + 1]

            if distance2 - distance1 == 0.0:
                self.positions = np.append(
                    self.positions,
                    [np.array([position1[0], position1[1]])],
                    axis=0,
                )
            else:
                multiplying_factor = (i - distance1) / (distance2 - distance1)
                self.positions = np.append(
                    self.positions,
                    [np.array(
                        [(position1[0]
                         + multiplying_factor
                         * (position2[0] - position1[0])),
                         (position1[1]
                         + multiplying_factor
                         * (position2[1] - position1[1])),
                         ]),
                     ],
                    axis=0,
                )

        self.positions = self.positions[::interval_distance]
        self.distances = self.distances[::interval_distance]

    def is_dead_end(
        self,
        azimuth_1: float,
        azimuth_2: float,
        tolerance_azimuth: float,
    ) -> bool:
        """Method for checking whether two azimuths represent a
        part of a dead end allowing the given tolerance.\n
        Args:
            azimuth_1 (float):
                first azimuth
            azimuth_2 (float):
                second azimuth
            tolerance_azimuth (float):
                difference tolerance of the two azimuths
        Returns:
            bool: True if given azimuths are within the given tolerance,
                  False otherwise.
        """
        if abs(180 - abs(azimuth_1 - azimuth_2)) < tolerance_azimuth:
            return True
        return False

    def long_enough_to_be_a_dead_end(
        self,
        start_distance: float,
        finish_distance: float,
    ) -> bool:
        """Method for checking whether a dead end is
        long enough to be a dead end.\n
        Args:
            start_distance (float):
                cummulative distance at the start of the dead end
            finish_distance (float):
                cummulative distance at the end of the dead end
        Returns:
            bool: True if dead end is long enough, False otherwise.
        """
        if finish_distance - start_distance < self.minimum_distance:
            return False
        return True

    def really_is_dead_end(
        self,
        position1: np.array,
        position2: np.array,
        tolerance_coordinates: float,
    ) -> bool:
        """Method for checking whether a dead end really is a dead end.\n
        Args:
            position1 (np.array):
                position of the first point
            position2 (np.array):
                position of the second point
            tolerance_coordinates (float):
                the tolerance between the two positions in meters
        Returns:
            bool: True if a track segment is a part of dead end,
                  False otherwise.
        """
        print(geopy.distance.distance(position1, position2).m)
        if (geopy.distance.distance(position1, position2).m
                < tolerance_coordinates):
            return True

        return False

    def identify_dead_ends(self) -> None:
        """Method for identifying dead ends of the exercise."""
        azimuths = np.array([])
        self.dead_ends = np.empty((0, 2), int)

        # Calculating the azimuths between the pairs of positions.
        # https://www.omnicalculator.com/other/azimuth#how-to-calculate-the-azimuth-from-latitude-and-longitude
        for i in np.arange(1, np.shape(self.positions)[0]):
            latitude1 = self.positions[i - 1][0]
            latitude2 = self.positions[i][0]
            longitude1 = self.positions[i - 1][1]
            longitude2 = self.positions[i][1]
            longitude_difference = longitude2 - longitude1
            azimuth = math.atan2(
                (math.sin(longitude_difference)
                 * math.cos(latitude2)
                 ),
                (math.cos(latitude1)
                 * math.sin(latitude2)
                 - math.sin(latitude1)
                 * math.cos(latitude2)
                 * math.cos(longitude_difference)
                 ),
            )
            azimuth *= 180 / math.pi  # Converting the azimuth to degrees.
            # If the azimuth's value is negative, the conversion to a
            # positive value is crucial in the next step of the algorithm.
            if azimuth < 0:
                azimuth += 360
            azimuths = np.append(azimuths, azimuth)

        # Checking for dead ends in the exercise.
        i = self.U_turn_allowed_distance
        while i < np.shape(azimuths)[0]:
            # Printing progress to console.
            print(f'\rProgress: {100 * i // np.shape(azimuths)[0]} %', end='')

            for j in np.arange(self.U_turn_allowed_distance):
                try:
                    if self.is_dead_end(
                        azimuths[i - j - 1],
                        azimuths[i + j],
                        self.tolerance_degrees,
                    ):
                        previous = i - j - 2
                        next = i + j + 1
                        while self.is_dead_end(
                            azimuths[previous],
                            azimuths[next],
                            self.tolerance_degrees,
                        ):
                            previous -= 1
                            next += 1

                        if np.array([previous, next]) not in self.dead_ends:
                            if self.long_enough_to_be_a_dead_end(
                                self.distances[previous],
                                self.distances[next],
                            ):
                                self.dead_ends = np.append(
                                    self.dead_ends,
                                    [np.array([previous, next])],
                                    axis=0,
                                )
                except Exception:
                    pass
            i += 1

        print(self.dead_ends)

        # Merging the dead ends.
        # while i < number_of_dead_ends:
        #  # Retrieving the last index in the previous interval.
        # # Retrieving the first index in the current interval.

        #     # If the distance between two dead ends is
        # less than 300 meters, the two dead ends are combined.
        #     if first_element - last_element < 300:
        #  # Current interval is removed from the list


        # Removing the dead ends which are too
        # short to be counted as dead ends.
        # while i < np.shape(self.dead_ends)[0]:
        #     if not self.long_enough_to_be_a_dead_end(
        # self.distances[self.dead_ends[i][1]]):

        # Removing the dead ends which are not dead ends.
        # while i < np.shape(self.dead_ends)[0]:
        #     print(np.linalg.norm(self.positions[self.dead_ends[i][0]] -
        # self.positions[self.dead_ends[i][1]]))
        #     if np.linalg.norm(self.positions[self.dead_ends[i][0]] -
        # self.positions[self.dead_ends[i][1]]) > self.tolerance_position:


        print('\rProgress: 100 %')

    def draw_map(self) -> None:
        """Method for visualisation of the exercise with identified dead ends."""
        plot = self.show_map()
        plot.show()

    def show_map(self) -> plt:
        """Method for plotting the exercise with dead ends.

        Returns
        -------
            plt.
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
            extent=(
                np.min(longitudes),
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

        # If there are some points inside the given area, the
        # segments outside and inside of the area are plotted
        # on the map.
        if np.shape(self.dead_ends)[0] > 0:
            # Drawing the starting path with no dead end.
            x, y = zip(
                *(map.rev_geocode(self.positions[p][::-1])
                  for p in np.arange(
                      0,
                      self.dead_ends[0][0] + 1,
                  )),
            )
            ax.plot(x, y, c='blue', label='No dead end')

            # Drawing the path within the dead end.
            for i in np.arange(np.shape(self.dead_ends)[0]):
                x, y = zip(
                    *(map.rev_geocode(self.positions[p][::-1])
                      for p in np.arange(
                          self.dead_ends[i][0],
                          self.dead_ends[i][1] + 1,
                      )),
                )

                if i == 0:
                    ax.plot(x, y, c='red', label='Dead end')
                else:
                    ax.plot(x, y, c='green', label='_nolegend_')

                if np.shape(self.dead_ends)[0] > i + 1:
                    x, y = zip(
                        *(map.rev_geocode(self.positions[p][::-1])
                          for p in np.arange(
                              self.dead_ends[i][1],
                              self.dead_ends[i + 1][0] + 1,
                          )),
                    )
                    ax.plot(x, y, c='blue', label='_nolegend_')

            # Drawing the ending path with no dead end.
            x, y = zip(
                *(map.rev_geocode(self.positions[p][::-1])
                  for p in np.arange(
                      self.dead_ends[-1][1],
                      np.shape(self.positions)[0],
                  )),
            )
            ax.plot(x, y, c='blue', label='_nolegend_')
        # If there are no points inside the given area,
        # the whole path is plotted as outside of the
        # given area.
        else:
            x, y = zip(
                *(map.rev_geocode(self.positions[p][::-1])
                  for p in np.arange(np.shape(self.positions)[0])),
            )
            ax.plot(x, y, c='blue', label='No dead end')

        ax.legend()
        plt.axis('off')
        plt.xlim((0, size))
        plt.ylim((size, 0))
        return plt
