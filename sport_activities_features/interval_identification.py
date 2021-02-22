import copy
import math

class IntervalIdentification(object):

    # To identify intervals, distances, timestamps, altitudes and mass are needed
    def __init__(self, distances, timestamps, altitudes, mass):
        self.distances = distances
        self.timestamps = timestamps
        self.altitudes = altitudes
        self.mass = mass  # Mass should be given in kilograms

    # Identifying intervals from given data
    def identify_intervals(self):
        self.intervals = []
        powers = []
        power_sum = 0.0

        # Loop to go through all segments and to calculate the average power
        for i in range(1, len(self.distances)):
            distance = self.distances[i] - self.distances[i - 1]  # Calculating the distance between two measures
            time = (self.timestamps[i] - self.timestamps[i - 1]).total_seconds()  # Calculating time between two measures
            speed = distance / time  # Calculating the average speed between two measures
            altitude_change = self.altitudes[i] - self.altitudes[i - 1]  # Calculating the change of altitude between two measures

            # Typical rolling resistance coefficient is 0.005, if multiplied by
            # mass and speed, the outcome is power to overcome the rolling resistance
            rolling_resistance_power = 0.005 * self.mass * speed

            # To calculate the gradient, flat distance is needed
            flat_distance = math.sqrt(abs(distance ** 2 - altitude_change ** 2))  # Calculation of the flat distance (according to the Pythagoras' theorem)

            if flat_distance == 0.0:
                gravity_power = 0.0
            else:
                gradient = altitude_change / flat_distance  # Gradient in percent is calculated as height change divided by flat distance

                # Average gravitational force is 9,81 m/s**2, if multiplied by mass, speed
                # and gradient, the outcome is power to overcome gravity (on hills)
                gravity_power = 9.81 * self.mass * speed * gradient

            # Total power is the sum of rolling resistance power and gravity power
            total_power = rolling_resistance_power + gravity_power

            # If total power is negative, it is set to zero
            if total_power < 0:
                total_power = 0

            powers.append(total_power)
            power_sum += total_power

        # Calculation of the average power
        average_power = power_sum / len(self.distances)

        interval = []
        counter = 0

        # Identifying the intervals
        for i in range(len(self.distances) - 1):
            # If the power is greater than the average power, the interval is recognized
            if powers[i] > average_power:
                interval.append(i)
            else:
                # If interval is not empty, it is appended to the list of all intervals
                if interval:
                    interval_flag = False

                    # Checking 200 measures in advance (if the interval continues)
                    for j in range(200):
                        try:
                            if powers[i + j] > average_power:  # If the interval continues in advance, it is added as one interval
                                interval_flag = True
                                interval.append(i)
                                break
                        except:
                            break

                    # If the interval is over, it is added to the list of all intervals
                    if interval_flag == False:
                        self.intervals.append(copy.deepcopy(interval))
                        interval.clear()

    # Returning all found intervals
    def return_intervals(self):
        return self.intervals