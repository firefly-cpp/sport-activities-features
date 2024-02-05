import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')


class PlotData:

    """Class for plotting the extracted data."""

    def get_positions_of_hills(self, identified_hills: list) -> list:
        """Method for retrieving positions of identified hills.\n
        Args:
            identified_hills (list):
                list of identified hills
        Returns:
            list: list of hills.
        """
        points = []
        for i in range(len(identified_hills)):
            for j in range(len(identified_hills[i])):
                points.append(identified_hills[i][j])
        return points

    def get_positions_of_intervals(self, identified_intervals: list) -> list:
        """Method for retrieving positions of identified intervals.\n
        Args:
            identified_intervals (list):
                list of identified intervals
        Returns:
            list: list of intervals.
        """
        points = []
        for i in range(len(identified_intervals)):
            for j in range(len(identified_intervals[i])):
                points.append(identified_intervals[i][j])
        return points

    def draw_hills_in_map(
        self,
        altitude: list,
        distance: list,
        identified_hills: list,
    ) -> None:
        """Method for plotting all hills identified in data
        on topographic map and rendering the plot.\n
        Args:
            altitude (list):
                list of altitudes
            distance (list):
                list of distances
            identified_hills (list):
                list of identified hills.
        """
        plt = self.plot_hills_on_map(altitude, distance, identified_hills)
        plt.show()

    def draw_intervals_in_map(
        self,
        timestamp: list,
        distance: list,
        identified_intervals: list,
    ) -> None:
        """Method for plotting all intervals identified in data
        on topographic map and rendering the plot.\n
        Args:
            timestamp (datetime):
                list of timestamps
            distance (float):
                list of distances
            identified_intervals (list):
                list of identified intervals.
        """
        plt = self.plot_intervals_in_map(timestamp, identified_intervals)
        plt.show()

    def draw_basic_map(self) -> None:
        """Method for plotting the whole topographic map and rendering the plot."""
        plt = self.plot_basic_map()
        plt.show()

    def plot_hills_on_map(
        self,
        altitude: list,
        distance: list,
        identified_hills: list,
    ) -> plt:
        """Method for plotting all hills identified in data on topographic map.\n
        Args:
            altitude (list):
                list of altitudes
            distance (list):
                list of distances
            identified_hills (list):
                list of identified hills
        Returns:
            plt.
        """
        y = []
        x = []

        current_hill = 0

        points = self.get_positions_of_hills(identified_hills)

        for j in range(len(distance)):
            y.append(float(altitude[j]))
            x.append(float(distance[j]))

            if j == 0:
                plt.plot(
                    [x[j], x[j]],
                    [0, y[j] + 20],
                    color='#000000',
                    markersize=5,
                )
                continue

            if (j - 1) == identified_hills[current_hill][0]:
                plt.plot(
                    [x[j-1], x[j-1]],
                    [0, y[j-1]+20],
                    color='#000000',
                    markersize=5,
                )
                if current_hill + 1 < len(identified_hills):
                    current_hill = current_hill + 1

            color = self.get_color_for_incline(x[j-1], x[j], y[j-1], y[j])
            if (j - 1) in points and j in points:
                plt.plot(
                    [x[j - 1], x[j]],
                    [y[j - 1], y[j]],
                    color=color,
                    markersize=5,
                )
                plt.fill_between([x[j-1], x[j]], [y[j-1], y[j]], 0, color=color, alpha=1)
            else:
                plt.plot(
                    [x[j - 1], x[j]],
                    [y[j - 1], y[j]],
                    color=color,
                    markersize=5,
                )
                plt.fill_between([x[j-1], x[j]], [y[j-1], y[j]], 0, color=color, alpha=1)

        plt.xticks(fontsize=14)
        plt.title('Detected hills', fontsize=20)
        plt.xlabel('Distance (m)', fontsize=20)
        plt.ylabel('Altitude (m)', fontsize=20)
        return plt

    def plot_intervals_in_map(
        self,
        timestamp: list,
        identified_intervals: list,
    ) -> plt:
        """Method for plotting all intervals identified
        in data on topographic map.\n
        Args:
            timestamp (list):
                list of timestamps
            identified_intervals (list):
                list of identified intervals
        Returns:
            plt.
        """
        x_points = []
        y_points = []

        points = self.get_positions_of_intervals(
            identified_intervals,
        )  # Getting positions of intervals

        # Appending points to lists
        for i in range(len(timestamp)):
            time = (
                    timestamp[i] - timestamp[0]
            ).total_seconds()
            # Calculation of time between the current and the starting point

            x_points.append(float(time))  # Appending the time to the list

            # If the current is in the list, it belongs to an interval
            if i > 0 and i in points:
                y_points.append(1)

                # If both current and previous point belong to
                # an interval, they are represented with red
                if y_points[i - 1] == y_points[i]:
                    plt.plot(
                        [x_points[i - 1], x_points[i]],
                        [y_points[i - 1], y_points[i]],
                        c='red',
                        linewidth=3,
                    )
            else:
                y_points.append(0)

                # If both current and previous point don't belong to
                # an interval, they are represented with blue
                if y_points[i - 1] == y_points[i]:
                    plt.plot(
                        [x_points[i - 1], x_points[i]],
                        [y_points[i - 1], y_points[i]],
                        c='blue',
                        linewidth=3,
                    )

        # Setting the parameters of the plot
        plt.xticks(fontsize=14)
        plt.yticks([0, 1], ['No', 'Yes'])
        plt.title('Intervals', fontsize=20)
        plt.xlabel('Time (s)', fontsize=20)
        plt.ylabel('Interval', fontsize=20)
        return plt

    def plot_basic_map(self, altitude: list, distance: list) -> plt:
        """Method for plotting the whole topographic map.\n
        Args:
            altitude (list):
                list of altitudes
            distance (list):
                list of distances
        Returns:
            plt.
        """
        ax = plt.axes()
        y = []
        x = []

        for j in range(len(distance)):
            y.append(float(altitude[j]))
            x.append(float(distance[j]))

            ax.plot(x[j], y[j], 'o', color='b', markersize=2)

        plt.xticks(fontsize=14)
        plt.title('Topographic map of cycling activity', fontsize=20)
        plt.xlabel('Distance (m)', fontsize=20)
        plt.ylabel('Altitude (m)', fontsize=20)
        return plt

    def get_color_for_incline(self, x1, x2, y1, y2) -> str:
        dy = y2 - y1
        dx = x2 - x1

        if dx == 0.0:
            incline = 0.0
        else:
            incline = (dy / dx) * 100

        incline = abs(incline)

        if incline == 0.0:
            return '#5FD67B'
        elif 0 < incline <= 2.9:
            return '#43C160'
        elif 2.9 < incline <= 5.9:
            return '#28A745'
        elif 5.9 < incline <= 8.9:
            return '#159231'
        elif incline > 8.9:
            return '#087621'
        else:
            return '#000000'
