import math

class IntervalIdentification(object):

    # To identify intervals, distances, timestamps, altitudes, mass and threshold are needed
    def __init__(self, distances, timestamps, altitudes, mass, threshold):
        self.distances = distances
        self.timestamps = timestamps
        self.altitudes = altitudes
        self.mass = mass  # Mass should be given in kilograms
        self.threshold = threshold  # Threshold should be given in percent (for example 30 % greater strength than average)

    # Identifying intervals from given data
    def identify_intervals(self):
        self.intervals = []
        average_power = 0.0

        # Loop to go through all segments and to identify intervals
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

            raise NotImplementedError

    # Returning all found intervals
    def return_intervals(self):
        raise NotImplementedError