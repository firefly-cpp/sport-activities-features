import math
import warnings

import geopy.distance
import matplotlib.pyplot as plt
import numpy as np


# Mean Earth radius in meters.
EARTH_RADIUS = 6371008.8


def _to_metres(positions: np.ndarray) -> np.ndarray:
    """Project (latitude, longitude) pairs to x, y in meters
    (equirectangular projection around the mean latitude). Distances
    between nearby points are accurate to well under a percent."""
    latitude = np.radians(np.mean(positions[:, 0]))
    return np.column_stack([
        EARTH_RADIUS * np.radians(positions[:, 1]) * math.cos(latitude),
        EARTH_RADIUS * np.radians(positions[:, 0]),
    ])


class DeadEndIdentification:

    """Class for identifying and visualising dead ends in an exercise.
    Dead end is a part of an exercise, where an athlete makes a U-turn
    and takes the same path as before the U-turn in the opposite
    direction.\n
    The exercise is resampled to one point per meter of distance. A U-turn
    is a point where the positions U_turn_allowed_distance meters before
    and after it are within tolerance_position meters of each other. From
    there the dead end is extended for as long as every point on the way
    back lies within tolerance_position meters of the way out (allowing
    U_turn_allowed_distance meters of shift along the path, because the
    measured distances out and back differ slightly). Dead ends shorter
    than minimum_distance (one way) are dropped and overlapping ones are
    merged.\n
    Args:
        positions (np.array):
            array of positions as pairs of latitudes and longitudes
        distances (np.array):
            array of cumulative distances in meters
        tolerance_degrees (float):
            deprecated and not used
        tolerance_position (float):
            maximum distance in meters between the way out and the way back
        minimum_distance (int):
            minimum length of a dead end in meters, one way
        U_turn_allowed_distance (int):
            maximum distance of a U-turn while turning around and starting
            a dead end, in meters
    """

    def __init__(
        self,
        positions: np.array,
        distances: np.array,
        tolerance_degrees: float = None,
        tolerance_position: float = 20.0,
        minimum_distance: int = 500,
        U_turn_allowed_distance: int = 50,
    ) -> None:
        """Initialisation method for DeadEndIdentification class.

        Args:
        ----
            positions (np.array):
                array of positions as pairs of latitudes and longitudes
            distances (np.array):
                array of cumulative distances in meters
            tolerance_degrees (float):
                deprecated and not used
            tolerance_position (float):
                maximum distance in meters between the way out and the way
                back
            minimum_distance (int):
                minimum length of a dead end in meters, one way
            U_turn_allowed_distance (int):
                maximum distance of a U-turn while turning around and
                starting a dead end, in meters.
        """
        if tolerance_degrees is not None:
            warnings.warn(
                'tolerance_degrees is deprecated and not used: dead ends '
                'are identified from positions (tolerance_position).',
                DeprecationWarning,
                stacklevel=2,
            )
        # Reorganizing the exercise data in order to achieve better results.
        self.reorganize_exercise_data(positions, distances, interval_distance=1)
        self.tolerance_degrees = tolerance_degrees
        self.tolerance_position = tolerance_position
        self.minimum_distance = minimum_distance
        self.U_turn_allowed_distance = U_turn_allowed_distance
        self.dead_ends = np.empty((0, 2), int)

    def reorganize_exercise_data(
        self,
        positions: np.array,
        distances: np.array,
        interval_distance: int = 1,
    ) -> None:
        """Method for reorganising the exercise in the way that the
        trackpoints are organized in a constant interval of distance.
        Points without a position or a distance are skipped.\n
        Args:
            positions (np.array):
                array of positions as pairs of latitudes and longitudes
            distances (np.array):
                array of cumulative distances
            interval_distance (int):
                desired distance between two neighboring points in meters.
        """
        positions = np.array(
            [[np.nan, np.nan] if p is None else p for p in positions],
            dtype=float,
        ).reshape(-1, 2)
        distances = np.array(
            [np.nan if d is None else d for d in distances], dtype=float,
        )
        valid = ~np.isnan(distances) & ~np.isnan(positions).any(axis=1)
        positions = positions[valid]
        # Cumulative distances must not decrease.
        distances = np.maximum.accumulate(distances[valid])

        if len(distances) < 2 or distances[-1] <= distances[0]:
            self.distances = np.array([])
            self.positions = np.empty((0, 2), float)
            return

        self.distances = np.arange(
            math.ceil(distances[0]), distances[-1], interval_distance,
        )
        self.positions = np.column_stack([
            np.interp(self.distances, distances, positions[:, 0]),
            np.interp(self.distances, distances, positions[:, 1]),
        ])

    def is_dead_end(
        self,
        azimuth_1: float,
        azimuth_2: float,
        tolerance_azimuth: float,
    ) -> bool:
        """Method for checking whether two azimuths are opposite
        allowing the given tolerance.\n
        Args:
            azimuth_1 (float):
                first azimuth in degrees
            azimuth_2 (float):
                second azimuth in degrees
            tolerance_azimuth (float):
                difference tolerance of the two azimuths
        Returns:
            bool:
              True, if given azimuths are within the given tolerance, False otherwise.
        """
        return abs(180 - abs(azimuth_1 - azimuth_2)) < tolerance_azimuth

    def long_enough_to_be_a_dead_end(
        self,
        start_distance: float,
        finish_distance: float,
    ) -> bool:
        """Method for checking whether a dead end is
        long enough to be a dead end.\n
        Args:
            start_distance (float):
                cumulative distance at the start of the dead end
            finish_distance (float):
                cumulative distance at the U-turn of the dead end
        Returns:
            bool:
              True, if dead end is long enough, False otherwise.
        """
        return finish_distance - start_distance >= self.minimum_distance

    def really_is_dead_end(
        self,
        position1: np.array,
        position2: np.array,
        tolerance_coordinates: float,
    ) -> bool:
        """Method for checking whether two positions are close enough to be
        on the way out and on the way back of a dead end.\n
        Args:
            position1 (np.array):
                position of the first point
            position2 (np.array):
                position of the second point
            tolerance_coordinates (float):
                the tolerance between the two positions in meters
        Returns:
            bool:
                True, if a track segment is a part of dead end, False otherwise.
        """
        return (
            geopy.distance.distance(position1, position2).m
            < tolerance_coordinates
        )

    def identify_dead_ends(self) -> np.ndarray:
        """Method for identifying dead ends of the exercise.\n
        Returns:
            np.ndarray: dead ends as [start_index, end_index] pairs of the
            reorganized exercise (self.positions, self.distances); also
            stored in self.dead_ends.
        """
        self.dead_ends = np.empty((0, 2), int)
        n = len(self.positions)
        u_turn = max(int(round(self.U_turn_allowed_distance)), 1)
        if n < 2 * u_turn + 1:
            return self.dead_ends

        xy = _to_metres(self.positions)
        tolerance = self.tolerance_position

        # U-turn candidates: the positions u_turn meters before and after
        # the point are close to each other.
        centres = np.arange(u_turn, n - u_turn)
        gaps = np.hypot(*(xy[centres - u_turn] - xy[centres + u_turn]).T)
        candidates = np.flatnonzero(gaps <= tolerance)
        if candidates.size == 0:
            return self.dead_ends

        found = []
        runs = np.split(candidates, np.flatnonzero(np.diff(candidates) > 1) + 1)
        for run in runs:
            turn = int(centres[run[np.argmin(gaps[run])]])
            length = self.__extend(xy, turn, u_turn, tolerance)
            if self.long_enough_to_be_a_dead_end(
                self.distances[turn - length], self.distances[turn],
            ):
                found.append((turn - length, turn + length))

        # Overlapping dead ends: keep the longest.
        kept = []
        for start, end in sorted(found, key=lambda d: d[0] - d[1]):
            if all(end <= s or start >= e for s, e in kept):
                kept.append((start, end))
        if kept:
            self.dead_ends = np.array(sorted(kept), dtype=int)
        return self.dead_ends

    @staticmethod
    def __extend(
        xy: np.ndarray, turn: int, u_turn: int, tolerance: float,
        chunk: int = 2000,
    ) -> int:
        """Number of points the dead end with the U-turn at index turn
        reaches in each direction: every point on the way back must lie
        within tolerance of a point on the way out that is at most u_turn
        points away from the mirrored position."""
        last = min(turn, len(xy) - 1 - turn)
        offsets = np.arange(-u_turn, u_turn + 1)
        length = u_turn
        while length < last:
            steps = np.arange(length + 1, min(length + chunk, last) + 1)
            way_back = xy[turn + steps]
            way_out = xy[np.clip(
                (turn - steps)[:, None] + offsets[None, :], 0, turn,
            )]
            nearest = np.hypot(
                *(way_out - way_back[:, None, :]).transpose(2, 0, 1),
            ).min(axis=1)
            too_far = np.flatnonzero(nearest > tolerance)
            if too_far.size:
                return int(steps[too_far[0]] - 1)
            length = int(steps[-1])
        return length

    def show_map(self) -> None:
        """Method for visualisation of the exercise with identified dead ends."""
        plot = self.plot_map()
        plot.show()

    def plot_map(self) -> plt:
        """Method for plotting the exercise with dead ends.

        Returns:        
            plt (matplotlib.pyplot):
                plot of the exercise with dead ends.
        """
        if np.shape(self.positions)[0] == 0:
            msg = 'Dataset is empty or invalid.'
            raise Exception(msg)

        # geotiler is only needed for the map, so it is imported here.
        import geotiler

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
