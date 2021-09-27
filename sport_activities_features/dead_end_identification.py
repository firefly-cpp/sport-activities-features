import math
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
    """

    def __init__(self, positions) -> None:
        """Initialization of the object.
        return: None
        """
        self.positions = np.array(positions)

    def identify_dead_ends(self) -> None:
        """Identifying dead ends of the exercise.
        return: None
        """
        azimuths = np.array([])

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

        raise NotImplementedError