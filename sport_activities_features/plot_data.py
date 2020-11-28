# %matplotlib inline
import geopy.distance
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


class PlotData(object):
    r"""Plotting the extracted data.

        """

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

    def draw_hills_in_map(self, altitude, distance, identified_hills):
        r"""Plot all hills identified in data on topographic map.

                """
        fig = plt.figure()
        ax = plt.axes()
        tocke = []
        tocke2 = []

        points = self.get_positions_of_hills(identified_hills)
        for j in range(len(distance)):
            tocke.append(float(altitude[j]))
            tocke2.append(float(distance[j]))

            if j in points:
                ax.plot(tocke2[j], tocke[j], 'o', color='r', markersize=2)

            else:
                ax.plot(tocke2[j], tocke[j], 'o', color='b', markersize=2)

        plt.xticks(fontsize=14)
        plt.title('Detected hills', fontsize=20)
        plt.xlabel('Distance (m)', fontsize=20)
        plt.ylabel('Altitude (m)', fontsize=20)
        plt.show()

    def draw_basic_map(self, altitude, distance):
        r"""Plot the whole topographic map.

                """
        fig = plt.figure()
        ax = plt.axes()
        tocke = []
        tocke2 = []

        for j in range(len(distance)):
            tocke.append(float(altitude[j]))
            tocke2.append(float(distance[j]))

            ax.plot(tocke2[j], tocke[j], 'o', color='b', markersize=2)

        plt.xticks(fontsize=14)
        plt.title('Topographic map of cycling activity', fontsize=20)
        plt.xlabel('Distance (m)', fontsize=20)
        plt.ylabel('Altitude (m)', fontsize=20)
        plt.show()
