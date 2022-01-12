# %matplotlib inline
import matplotlib.pyplot as plt

plt.style.use("seaborn-whitegrid")


class PlotData(object):
    r"""Plotting the extracted data."""

    def get_positions_of_hills(self, identified_hills):
        r"""Return positions of identified hills.

        Returns:
            str: Array
        """
        points = []
        for i in range(len(identified_hills)):
            for j in range(len(identified_hills[i])):
                points.append(identified_hills[i][j])
        return points

    def get_positions_of_intervals(self, identified_intervals):
        r"""Return positions of identified intervals.

        Returns:
            str: Array
        """
        points = []
        for i in range(len(identified_intervals)):
            for j in range(len(identified_intervals[i])):
                points.append(identified_intervals[i][j])
        return points

    def draw_hills_in_map(self, altitude, distance, identified_hills):
        r"""Plot all hills identified in data on topographic map. Renders the plot."""
        plt = self.plot_hills_on_map(altitude, distance, identified_hills)
        plt.show()

    def draw_intervals_in_map(self, timestamp, distance, identified_intervals):
        """Plot all intervals identified in data on topographic map. Renders the plot."""
        plt = self.plot_intervals_in_map(self, timestamp, distance, identified_intervals)
        plt.show()

    def draw_basic_map(self, altitude, distance):
        r"""Plot the whole topographic map. Renders the plot."""
        plt = self.plot_basic_map()
        plt.show()

    def plot_hills_on_map(self, altitude, distance, identified_hills):
        r"""Plot all hills identified in data on topographic map. Returns plot object."""
        fig = plt.figure()
        ax = plt.axes()
        tocke = []
        tocke2 = []

        points = self.get_positions_of_hills(identified_hills)
        for j in range(len(distance)):
            tocke.append(float(altitude[j]))
            tocke2.append(float(distance[j]))

            if j == 0:
                continue

            if (j - 1) in points and j in points:
                plt.plot(
                    [tocke2[j - 1], tocke2[j]],
                    [tocke[j - 1], tocke[j]],
                    color="r",
                    markersize=5,
                )
            else:
                plt.plot(
                    [tocke2[j - 1], tocke2[j]],
                    [tocke[j - 1], tocke[j]],
                    color="b",
                    markersize=5,
                )

        plt.xticks(fontsize=14)
        plt.title("Detected hills", fontsize=20)
        plt.xlabel("Distance (m)", fontsize=20)
        plt.ylabel("Altitude (m)", fontsize=20)
        return plt

    # Drawing the map with the intervals
    def plot_intervals_in_map(self, timestamp, distance, identified_intervals):
        r"""Plot all intervals identified in data on topographic map. Returns plot object"""
        fig = plt.figure("Intervals")
        ax = plt.axes()
        x_points = []
        y_points = []
        colors = []

        points = self.get_positions_of_intervals(
            identified_intervals
        )  # Getting positions of intervals

        # Appending points to lists
        for i in range(len(timestamp)):
            time = (
                    timestamp[i] - timestamp[0]
            ).total_seconds()  # Calculation of time between the current and the starting point

            x_points.append(float(time))  # Appending the time to the list

            # If the current is in the list, it belongs to an interval
            if i > 0 and i in points:
                y_points.append(1)

                # If both current and previous point belong to an interval, they are represented with red
                if y_points[i - 1] == y_points[i]:
                    plt.plot(
                        [x_points[i - 1], x_points[i]],
                        [y_points[i - 1], y_points[i]],
                        c="red",
                        linewidth=3,
                    )
            else:
                y_points.append(0)

                # If both current and previous point don't belong to an interval, they are represented with blue
                if y_points[i - 1] == y_points[i]:
                    plt.plot(
                        [x_points[i - 1], x_points[i]],
                        [y_points[i - 1], y_points[i]],
                        c="blue",
                        linewidth=3,
                    )

        # Setting the parameters of the plot
        plt.xticks(fontsize=14)
        plt.yticks([0, 1], ["No", "Yes"])
        plt.title("Intervals", fontsize=20)
        plt.xlabel("Time (s)", fontsize=20)
        plt.ylabel("Interval", fontsize=20)
        return plt

    def plot_basic_map(self, altitude, distance):
        r"""Plot the whole topographic map. Returns plot object."""
        fig = plt.figure()
        ax = plt.axes()
        tocke = []
        tocke2 = []

        for j in range(len(distance)):
            tocke.append(float(altitude[j]))
            tocke2.append(float(distance[j]))

            ax.plot(tocke2[j], tocke[j], "o", color="b", markersize=2)

        plt.xticks(fontsize=14)
        plt.title("Topographic map of cycling activity", fontsize=20)
        plt.xlabel("Distance (m)", fontsize=20)
        plt.ylabel("Altitude (m)", fontsize=20)
        return plt
