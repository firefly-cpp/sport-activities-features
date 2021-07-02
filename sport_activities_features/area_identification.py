import numpy as np
from numpy.lib.function_base import average

class AreaIdentification(object):
    r"""Area identification based by coordinates.
    
    Date:
        2021

    Author:
        Luka Lukač

    License:
        MIT
    
    Attributes:
        None
    """

    def __init__(self, positions, distances, timestamps, heartrates, area_coordinates) -> None:
        """ Initialization of the object.
            return: None
        """
        self.positions = np.array(positions)
        self.distances = np.array(distances)
        self.timestamps = np.array(timestamps)
        self.heartrates = np.array(heartrates)
        self.area_coordinates = np.array(area_coordinates)

    def is_equal(self, value1, value2) -> bool:
        """ Checking whether the two values are equal with certain tolerance.
            return: bool
        """
        tolerance = 0.00001

        # If the absolute value of substraction is smaller than the tolerance threshold,
        # the two values are counted as equal.
        if abs(value1 - value2) < tolerance:
            return True
        
        return False

    def do_two_lines_intersect(self, p1, p2, p3, p4) -> bool:
        """ Checking whether two lines have an intersection point.
            return: bool
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

        # If the intersection point is in the middle of the line segment, the intersection is counted.
        if Ua > 0 and Ua < 1 and Ub > 0 and Ub < 1:
            return True
        elif self.is_equal(Ua, 0):
            return True
        
        return False

    def identify_points_in_area(self) -> None:
        """ Identifying the measure points of the activity inside the specified area.
            return: None
        """
        self.points_in_area = np.array([])

        # Checking whether coordinates are inside the given area.
        for i in np.arange(1, np.shape(self.positions)[0]):
            number_of_intersections = 0

            # If the ray intersects with the area even times, the point is not inside area.
            for border in np.arange(np.shape(self.area_coordinates)[0]):
                for j in np.arange(-1, np.shape(self.area_coordinates[border])[0] - 1):
                    if self.do_two_lines_intersect(self.area_coordinates[border][j], self.area_coordinates[border][j + 1], np.array([self.positions[i][0], self.positions[i][1]]), np.array([190, self.positions[i][1]])):
                        number_of_intersections += 1

            # If the number of intersections is odd, the point is inside the given area.
            if number_of_intersections % 2 == 1:
                self.points_in_area = np.append(self.points_in_area, int(i))

        self.points_in_area = self.points_in_area.astype('int32')

    def extract_data_in_area(self) -> dict:
        """ Extracting the data of the identified points in area.
            return: dict
        """
        distance = 0.0
        time = 0.0
        max_speed = 0.0
        heartrates = np.array([])

        # Extracting the data from the identified points.
        for i in self.points_in_area:
            cur_distance = self.distances[i] - self.distances[i - 1]
            cur_time = (self.timestamps[i] - self.timestamps[i - 1]).seconds
            distance += cur_distance
            time += cur_time
            if self.heartrates[i]: 
                heartrates = np.append(heartrates, self.heartrates[i])
            if cur_distance / cur_time > max_speed:
                max_speed = cur_distance / cur_time

        return {
            'distance': distance,
            'time': time,
            'max_speed': max_speed,
            'avg_speed': distance / time,
            'min_heartrate': np.min(heartrates),
            'max_heartrate': np.max(heartrates),
            'avg_heartrate': np.sum(heartrates) / np.size(heartrates),
        }