import geotiler
import math
import matplotlib.pyplot as plt
import numpy as np


class DeadEndIdentification(object):
    r"""Dead end identification based on coordinates.

    Date:
        2021

    Author:
        Luka Lukač

    License:
        MIT

    Attributes:
        None

    Description:
        This module is intended to be used for the identification and visualization of dead ends in an exercise.
        Dead end is a part of an exercise, where an athlete suddenly makes a U-turn and takes the same path as before the U-turn is conducted (in the opposite direction).
    """

    def __init__(self, positions, distances, tolerance_degrees=5, minimum_distance=500) -> None:
        """Initialization of the object.
        return: None
        """
        self.positions = np.array(positions)
        self.distances = np.array(distances)
        self.tolerance_degrees = tolerance_degrees
        self.minimum_distance = minimum_distance

    def is_dead_end(self, azimuth1, azimuth2, tolerance) -> bool:
        """Checking if two azimuths represent a part of a dead end allowing the given tolerance.
        return: bool
        """
        if abs(180 - abs(azimuth1 - azimuth2)) < tolerance:
            return True

        return False

    def long_enough_to_be_a_dead_end(self, distance1, distance2) -> bool:
        """Checking whether a dead end is long enough to be a dead end.
        return: bool
        """
        if distance2 - distance1 < self.minimum_distance:
            return False

        return True

    def identify_dead_ends(self) -> None:
        """Identifying dead ends of the exercise.
        return: None
        """
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
            azimuth = math.atan2(math.sin(longitude_difference) * math.cos(latitude2),
                                 math.cos(latitude1) * math.sin(latitude2) - math.sin(latitude1) * math.cos(latitude2) * math.cos(longitude_difference))
            azimuth *= 180 / math.pi  # Converting the azimuth to degrees.
            # If the azimuth's value is negative, the conversion to a positive value is crucial in the next step of the algorithm.
            if azimuth < 0:
                azimuth += 360
            azimuths = np.append(azimuths, azimuth)

        # Checking for dead ends in the exercise.
        for i in np.arange(1, np.shape(azimuths)[0]):
            if self.is_dead_end(azimuths[i - 1], azimuths[i], self.tolerance_degrees):
                previous = i - 2
                next = i + 1
                while self.is_dead_end(azimuths[previous], azimuths[next], self.tolerance_degrees):
                    previous -= 1
                    next += 1

                self.dead_ends = np.append(self.dead_ends, [np.array([previous, next])], axis=0)

        # Removing the dead ends which are too short to be counted as dead ends.
        for i in np.arange(np.shape(self.dead_ends)[0]):
            if not self.long_enough_to_be_a_dead_end(self.distances[self.dead_ends[i][0]], self.distances[self.dead_ends[i][1]]):
                self.dead_ends = np.delete(self.dead_ends, i, 0)
                i -= 1

    def draw_map(self) -> None:
        """ Visualization of the exercise with dead ends.
            return: none
        """
        plot = self.show_map()
        plot.show()

    def show_map(self) -> None:
        """ Identification of the exercise with dead ends.
            return: plt
        """
        if np.shape(self.positions)[0] == 0:
            raise Exception('Dataset is empty or invalid.')

        # Downloading the map.
        size = 10000
        coordinates = self.positions.flatten()
        latitudes = coordinates[::2]
        longitudes = coordinates[1::2]
        map = geotiler.Map(extent=(np.min(longitudes), np.min(latitudes), np.max(longitudes), np.max(latitudes)),
                           size=(size, size))
        image = geotiler.render_map(map)

        # Drawing the map as plot.
        ax = plt.subplot(111)
        ax.imshow(image)

        # If there are some points inside the given area, the segments outside and inside of the area are plotted on the map.
        if np.shape(self.dead_ends)[0] > 0:
            # Drawing the starting path with no dead end.
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in np.arange(0, self.dead_ends[0][0] + 1)))
            ax.plot(x, y, c='blue', label='No dead end')

            # Drawing the path within the dead end.
            for i in np.arange(np.shape(self.dead_ends)[0]):
                x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in
                             np.arange(self.dead_ends[i][0], self.dead_ends[i][1] + 1)))

                if i == 0:
                    ax.plot(x, y, c='red', label='Dead end')
                else:
                    ax.plot(x, y, c='red', label='_nolegend_')

                if np.shape(self.dead_ends)[0] > i + 1:
                    x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in
                                 np.arange(self.dead_ends[i][1], self.dead_ends[i + 1][0] + 1)))
                    ax.plot(x, y, c='blue', label='_nolegend_')

            # Drawing the ending path with no dead end.
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in
                         np.arange(self.dead_ends[-1][1], np.shape(self.positions)[0])))
            ax.plot(x, y, c='blue', label='_nolegend_')
        # If there are no points inside the given area, the whole path is plotted as outside of the given area.
        else:
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in np.arange(np.shape(self.positions)[0])))
            ax.plot(x, y, c='blue', label='No dead end')

        ax.legend()
        plt.axis('off')
        plt.xlim((0, size))
        plt.ylim((size, 0))

        return plt
