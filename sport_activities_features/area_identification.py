import geotiler
import numpy as np
import matplotlib.pyplot as plt


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

    def __init__(
        self, positions, distances, timestamps, heartrates, area_coordinates
    ) -> None:
        """Initialization of the object.
        return: None
        """
        self.positions = np.array(positions)
        self.distances = np.array(distances)
        self.timestamps = np.array(timestamps)
        self.heartrates = np.array(heartrates)
        self.area_coordinates = np.array(area_coordinates)

    def is_equal(self, value1, value2) -> bool:
        """Checking whether the two values are equal with certain tolerance.
        return: bool
        """
        tolerance = 0.00001

        # If the absolute value of substraction is smaller than the tolerance threshold,
        # the two values are counted as equal.
        if abs(value1 - value2) < tolerance:
            return True

        return False

    def do_two_lines_intersect(self, p1, p2, p3, p4) -> bool:
        """Checking whether two lines have an intersection point.
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

        return False

    def identify_points_in_area(self) -> None:
        """Identifying the measure points of the activity inside the specified area.
        return: None
        """
        self.points_in_area = np.array([])
        self.points_outside_area = np.array([])


        # Checking whether coordinates are inside the given area.
        for i in np.arange(np.shape(self.positions)[0]):
            number_of_intersections = 0

            # If the ray intersects with the area even times, the point is not inside area.
            for border in np.arange(np.shape(self.area_coordinates)[0]):
                for j in np.arange(-1, np.shape(self.area_coordinates[border])[0] - 1):
                    if self.do_two_lines_intersect(
                        self.area_coordinates[border][j],
                        self.area_coordinates[border][j + 1],
                        np.array([self.positions[i][0], self.positions[i][1]]),
                        np.array([190, self.positions[i][1]]),
                    ):
                        number_of_intersections += 1

            # If the number of intersections is odd, the point is inside the given area.
            if number_of_intersections % 2 == 1:
                self.points_in_area = np.append(self.points_in_area, int(i))
            else:
                self.points_outside_area = np.append(self.points_outside_area, int(i))

        self.points_in_area = self.points_in_area.astype('int32')
        self.points_outside_area = self.points_outside_area.astype('int32')

    def extract_data_in_area(self) -> dict:
        """Extracting the data of the identified points in area.
        return: dict
        """
        distance = 0.0
        time = 0.0
        max_speed = 0.0
        heartrates = np.array([])

        # Extracting the data from the identified points.
        for i in self.points_in_area:
            try:
                cur_distance = self.distances[i] - self.distances[i - 1]
                cur_time = (self.timestamps[i] - self.timestamps[i - 1]).seconds
                distance += cur_distance
                time += cur_time
                if self.heartrates[i]:
                    heartrates = np.append(heartrates, self.heartrates[i])
                if cur_time != 0.0 and cur_distance / cur_time > max_speed:
                    max_speed = cur_distance / cur_time
            except:
                pass

        try:
            avg_speed = distance / time
        except:
            avg_speed = 0.0
        
        try:
            min_heartrate = np.min(heartrates)
            max_heartrate = np.max(heartrates)
            avg_heartrate = np.sum(heartrates) / np.size(heartrates)
        except:
            min_heartrate = None
            max_heartrate = None
            avg_heartrate = None

        return {
            'distance': distance,
            'time': time,
            'max_speed': max_speed,
            'avg_speed': avg_speed,
            'min_heartrate': min_heartrate,
            'max_heartrate': max_heartrate,
            'avg_heartrate': avg_heartrate,
        }

    def draw_map(self) -> None:
        """ Visualization of the exercise.
            return: None
        """
        if np.shape(self.positions)[0] == 0:
            raise Exception('Dataset is empty or invalid.')

        # Downloading the map.
        size = 10000
        coordinates = self.positions.flatten()
        latitudes = coordinates[::2]
        longitudes = coordinates[1::2]
        map = geotiler.Map(extent=(np.min(longitudes), np.min(latitudes), np.max(longitudes), np.max(latitudes)), size=(size, size))
        image = geotiler.render_map(map)

        # Drawing the map as plot.
        ax = plt.subplot(111)
        ax.imshow(image)
        if np.shape(self.points_in_area)[0] > 0:
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in self.points_in_area))
            ax.plot(x, y, c='red', label='Inside area')
        if np.shape(self.points_outside_area)[0] > 0:
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in self.points_outside_area))
            ax.plot(x, y, c='blue', label='Outside area')

        # Drawing the bounding box of the chosen area.
        for hull in self.area_coordinates:
            x, y = zip(*(map.rev_geocode(hull[i - 1][::-1]) for i in np.arange(np.shape(hull)[0] + 1)))
            ax.plot(x, y, c='black', label='Area border')

        ax.legend()
        plt.axis('off')
        plt.xlim((0, size))
        plt.ylim((size, 0))
        plt.show()

    @staticmethod
    def draw_activities_inside_area_on_map(activities, area_coordinates) -> None:
        """ Drawing all activities inside area on map.
            return: None
        """
        # Downloading the map.
        size = 10000
        coordinates = area_coordinates.flatten()
        latitudes = coordinates[::2]
        longitudes = coordinates[1::2]
        map = geotiler.Map(extent=(np.min(longitudes), np.min(latitudes), np.max(longitudes), np.max(latitudes)), size=(size, size))
        image = geotiler.render_map(map)

        # Drawing the map as plot.
        ax = plt.subplot(111)
        ax.imshow(image)
           
        for i in np.arange(np.shape(activities)[0]):
            x, y = zip(*(map.rev_geocode(activities[i].positions[p][::-1]) for p in activities[i].points_in_area))
            ax.plot(x, y, label='Activity {}'.format(i + 1))

        # Drawing the bounding box of the chosen area.
        for hull in area_coordinates:
            x, y = zip(*(map.rev_geocode(hull[i - 1][::-1]) for i in np.arange(np.shape(hull)[0] + 1)))
            ax.plot(x, y, c='black', label='Area border')

        ax.legend()
        plt.axis('off')
        plt.xlim((0, size))
        plt.ylim((size, 0))
        plt.show()
