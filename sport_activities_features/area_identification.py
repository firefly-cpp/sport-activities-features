import numpy as np

class AreaIdentifiaction(object):
    def __init__(self, positions, distances, area_coordinates) -> None:
        """ Initialization of the object.
            return: None
        """
        self.positions = np.array(positions)
        self.distances = np.array(distances)
        self.area_coordinates = np.array(area_coordinates)

    def is_point_on_the_right_side_of_line_segment(self, point, linesegment_point1, linesegment_point2) -> bool:
        """ Checking whether the point is on the right side of the line, given with two points.
            return: bool
        """
        # Initializing the two vectors
        point = np.array(point)
        vector1 = np.array(point - linesegment_point1)
        vector2 = np.array(linesegment_point2 - linesegment_point1)

        cross_product = np.cross(vector1, vector2)  # Calculating the cross product between the two vectors

        # If the cross product is >=0, the point is on the right side of the line or on the line
        if cross_product >= 0:
            return True
        else:
            return False

    def identify_distance_in_area(self) -> float:
        """ Identifying the distance (in meters) of the activity inside the specified area
            return: float
        """
        distance_in_area = 0.0

        # Checking whether coordinates are inside the given area
        for i in np.arange(1, np.shape(self.positions)[0]):
            # If the point is on the right side of all vectors in polygone (going clockwise) with area end points,
            # we can assume with certainty that the point is inside that area
            for j in np.arange(-1, np.shape(self.area_coordinates)[0] - 1):
                # If point is not on the right side of a vector, we can assume it is not inside the area
                if not self.is_point_on_the_right_side_of_line_segment(self.positions[i], self.area_coordinates[j], self.area_coordinates[j + 1]) and \
                   not self.is_point_on_the_right_side_of_line_segment(self.positions[i - 1], self.area_coordinates[j], self.area_coordinates[j + 1]):
                    break
            else:
                distance_in_area += self.distances[i] - self.distances[i - 1]  # If the point is inside area, distance is added

        return distance_in_area