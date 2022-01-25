import geotiler
import numpy as np
import matplotlib.pyplot as plt


class AreaIdentification(object):
    r"""Area identification based by coordinates.

    Date:
        2021

    Author:
        Luka Lukač

    Reference:
        L. Lukač, "Extraction and Analysis of Sport Activity Data Inside Certain Area", 7th Student Computer Science Research Conference StuCoSReC, 2021, pp. 47-50, doi: https://doi.org/10.18690/978-961-286-516-0.9

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
        currently_in_area = False
        p1 = None

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
                if not currently_in_area:
                    p1 = int(i)
                    currently_in_area = True
            else:
                if currently_in_area:
                    self.points_in_area = np.append(self.points_in_area, (p1, int(i) - 1))
                    p1 = None
                    currently_in_area = False

        self.points_in_area = self.points_in_area.astype('int32')
        self.points_in_area = np.reshape(self.points_in_area, (-1, 2))

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
                cur_distance = self.distances[i][1] - self.distances[i][0]
                cur_time = (self.timestamps[i][1] - self.timestamps[i][0]).seconds
                distance += cur_distance
                time += cur_time
                if not np.isnan(self.heartrates[[i][0]:[i][1]]).any():
                    heartrates = np.append(heartrates, self.heartrates[[i][0]:[i][1]])
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
            'avg_speed': avg_speed,
            'min_heartrate': min_heartrate,
            'max_heartrate': max_heartrate,
            'avg_heartrate': avg_heartrate,
        }

    def plot_map(self):
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
        if np.shape(self.points_in_area)[0] > 0:
            # Drawing the starting path outside of the area.
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in np.arange(0, self.points_in_area[0][0] + 1)))
            ax.plot(x, y, c='blue', label='Outside of the area')

            # Drawing the path inside of the area and possible paths in between outside of the area.
            for i in np.arange(np.shape(self.points_in_area)[0]):
                x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in
                             np.arange(self.points_in_area[i][0], self.points_in_area[i][1] + 1)))

                if i == 0:
                    ax.plot(x, y, c='red', label='Inside of the area')
                else:
                    ax.plot(x, y, c='red', label='_nolegend_')

                if np.shape(self.points_in_area)[0] > i + 1:
                    x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in
                                 np.arange(self.points_in_area[i][1], self.points_in_area[i + 1][0] + 1)))
                    ax.plot(x, y, c='blue', label='_nolegend_')

            # Drawing the ending path outside of the area.
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in
                         np.arange(self.points_in_area[-1][1], np.shape(self.positions)[0])))
            ax.plot(x, y, c='blue', label='_nolegend_')
        # If there are no points inside the given area, the whole path is plotted as outside of the given area.
        else:
            x, y = zip(*(map.rev_geocode(self.positions[p][::-1]) for p in np.arange(np.shape(self.positions)[0])))
            ax.plot(x, y, c='blue', label='Outside of the area')

        # Drawing the bounding box of the chosen area.
        for hull in self.area_coordinates:
            x, y = zip(*(map.rev_geocode(hull[i - 1][::-1]) for i in np.arange(np.shape(hull)[0] + 1)))
            ax.plot(x, y, c='black', label='Area border')

        ax.legend()
        plt.axis('off')
        plt.xlim((0, size))
        plt.ylim((size, 0))
        return plt

    def draw_map(self) -> None:
        """ Visualization of the exercise.
            return: None
        """
        plt = self.plot_map()
        plt.show()

    @staticmethod
    def plot_activities_inside_area_on_map(activities, area_coordinates):
        size = 10000
        coordinates = area_coordinates.flatten()
        latitudes = coordinates[::2]
        longitudes = coordinates[1::2]
        map = geotiler.Map(extent=(np.min(longitudes), np.min(latitudes), np.max(longitudes), np.max(latitudes)), size=(size, size))
        image = geotiler.render_map(map)
        colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'key', 'white']

        # Drawing the map as plot.
        ax = plt.subplot(111)
        ax.imshow(image)
        for i in np.arange(np.shape(activities)[0]):
            sectors = np.array([])
            for j in np.arange(np.shape(activities[i].points_in_area)[0]):
                sectors = np.append(sectors, zip(*(map.rev_geocode(activities[i].positions[p][::-1]) for p in np.arange(activities[i].points_in_area[j][0], activities[i].points_in_area[j][1] + 1))))

            # Plotting each activity (displayed only once in legend).
            for j in np.arange(np.shape(sectors)[0]):
                x, y = sectors[j]
                if j == 0:
                    ax.plot(x, y, c=colors[i % 8], label='Activity {}'.format(i + 1))
                else:
                    ax.plot(x, y, c=colors[i % 8], label='_nolegend_')

        # Drawing the bounding box of the chosen area.
        for hull in area_coordinates:
            x, y = zip(*(map.rev_geocode(hull[i - 1][::-1]) for i in np.arange(np.shape(hull)[0] + 1)))
            ax.plot(x, y, c='black', label='Area border')

        ax.legend()
        plt.axis('off')
        plt.xlim((0, size))
        plt.ylim((size, 0))
        return plt

    @staticmethod
    def draw_activities_inside_area_on_map(activities, area_coordinates) -> None:
        """ Drawing all activities inside area on map.
            return: None
        """
        # Downloading the map.
        plt = AreaIdentification.plot_activities_inside_area_on_map(activities, area_coordinates)
        plt.show()
