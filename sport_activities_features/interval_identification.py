import copy
import math

import numpy


class IntervalIdentificationByPower(object):
    """
    Class for identifying intervals based on power.\n
    Args:
        distances (list):
            list of cummulative distances
        timestamps (list):
            list of timestamps
        altitudes (list):
            list of altitudes
        mass (int):
            total mass of an athlete given in kilograms
        minimum_time (int):
            minimum time of an interval given in seconds
    """

    def __init__(
        self,
        distances: list,
        timestamps: list,
        altitudes: list,
        mass: int,
        minimum_time: int = 30,
    ) -> None:
        """
        Initialisation method for IntervalIdentificationByPower class.\n
        Args:
            distances (list):
                list of cummulative distances
            timestamps (list):
                list of timestamps
            altitudes (list):
                list of altitudes
            mass (int):
                total mass of an athlete given in kilograms
            minimum_time (int):
                minimum time of an interval given in seconds
        """
        self.distances = distances
        self.timestamps = timestamps
        self.altitudes = altitudes
        self.mass = mass
        self.minimum_time = minimum_time

    def identify_intervals(self) -> None:
        """
        Method for identifying intervals from given data.
        """
        self.intervals = []
        powers = []
        power_sum = 0.0

        # Loop to go through all segments and to calculate the average power
        for i in range(1, len(self.distances)):
            distance = (
                self.distances[i] - self.distances[i - 1]
            )  # Calculating the distance between two measures
            time = (
                self.timestamps[i] - self.timestamps[i - 1]
            ).total_seconds()  # Calculating time between two measures
            if time == 0:
                powers.append(0)
                continue

            speed = (
                distance / time
            )  # Calculating the average speed between two measures
            altitude_change = (
                self.altitudes[i] - self.altitudes[i - 1]
            )  # Calculating the change of altitude between two measures

            # Typical rolling resistance coefficient is 0.005, if multiplied by
            # mass and speed, the outcome is power to overcome the rolling
            # resistance
            rolling_resistance_power = 0.005 * self.mass * speed

            # To calculate the gradient, flat distance is needed
            # Calculation of the flat distance
            # (according to the Pythagoras' theorem)
            flat_distance = math.sqrt(
                abs(distance**2 - altitude_change**2)
            )

            if flat_distance == 0.0:
                gravity_power = 0.0
            else:
                # Gradient in percent is calculated as height
                # change divided by flat distance
                gradient = altitude_change / flat_distance

                # Average gravitational force is 9,81 m/s**2, if
                # multiplied by mass, speed and gradient, the
                # outcome is power to overcome gravity (on hills)
                gravity_power = 9.81 * self.mass * speed * gradient

            # Total power is the sum of rolling
            # resistance power and gravity power
            total_power = rolling_resistance_power + gravity_power

            # If total power is negative, it is set to zero
            if total_power < 0:
                total_power = 0

            powers.append(total_power)
            power_sum += total_power

        # Calculation of the average power
        average_power = power_sum / len(self.distances)

        # Identifying the intervals by power
        # An interval is identified, when a segment's
        # power is greater than the average power
        interval = []
        for i in range(len(self.distances) - 1):
            # If the power is greater than the average power,
            # the interval is recognized
            if powers[i] > average_power:
                interval.append(i)
            else:
                # If interval is not empty, it is appended
                # to the list of all intervals
                if interval:
                    self.intervals.append(copy.deepcopy(interval))
                    interval.clear()

        # Combining intervals according to the time between them
        # Combining according to power can be very problematic,
        # since there is no good way of knowing when two or more
        # intervals could be merged into a common interval
        i = 1
        number_of_intervals = len(self.intervals) - 1
        while i < number_of_intervals:
            last_element = self.intervals[i - 1][
                -1
            ]  # Retrieving the last index in the previous interval
            first_element = self.intervals[i][
                0
            ]  # Retrieving the first index in the current interval

            # If time between two intervals is less than 30 seconds,
            # the two intervals are combined
            if (
                self.timestamps[first_element] - self.timestamps[last_element]
            ).total_seconds() < 30:
                # Indexes between the two intervals have
                # to be added to an interval
                self.intervals[i - 1].extend(
                    list(range(last_element + 1, first_element))
                )
                self.intervals[i - 1].extend(
                    self.intervals[i]
                )  # Current interval is added to the previous one
                self.intervals.remove(
                    self.intervals[i]
                )  # Current interval is removed from the list
                number_of_intervals -= 1
            else:
                i += 1

        # Removing intervals that are too short
        # (shorter than minimum_time, given as an argument)
        i = 0
        number_of_intervals = len(self.intervals) - 1
        while i < number_of_intervals:
            first_element = self.intervals[i][0]
            last_element = self.intervals[i][-1]

            # If an interval is shorter than self.minimum_time seconds,
            # it is removed
            if (
                self.timestamps[last_element] - self.timestamps[first_element]
            ).total_seconds() < self.minimum_time:
                self.intervals.remove(
                    self.intervals[i]
                )  # Current interval is removed from the list
                number_of_intervals -= 1
            else:
                i += 1

    def calculate_interval_statistics(self) -> dict:
        """
        Method for calculating interval statistics.\n
        Returns:
            data = {
                'number_of_intervals': number_of_intervals,
                'min_duration': min_duration_interval,
                'max_duration': max_duration_interval,
                'avg_duration': avg_duration_interval,
                'min_distance': min_distance_interval,
                'max_distance': max_distance_interval,
                'avg_distance': avg_distance_interval,
            }
        """
        number_of_intervals = len(self.intervals)  # Number of intervals

        list_duration = [
            (
                self.timestamps[item[-1]] - self.timestamps[item[0]]
            ).total_seconds()
            for item in self.intervals
        ]
        min_duration_interval = min(list_duration)
        max_duration_interval = max(list_duration)
        avg_duration_interval = sum(list_duration) / len(list_duration)

        list_distance = [
            self.distances[item[-1]] - self.distances[item[0]]
            for item in self.intervals
        ]  # Distance of every interval in list
        min_distance_interval = min(list_distance)
        max_distance_interval = max(list_distance)
        avg_distance_interval = sum(list_distance) / len(
            list_distance
        )  # Average distance of an interval

        # Building a dictionary
        data = {
            "number_of_intervals": number_of_intervals,
            "min_duration": min_duration_interval,
            "max_duration": max_duration_interval,
            "avg_duration": avg_duration_interval,
            "min_distance": min_distance_interval,
            "max_distance": max_distance_interval,
            "avg_distance": avg_distance_interval,
        }
        return data

    def return_intervals(self) -> list:
        """
        Method for retrieving identified intervals.\n
        Returns:
            list: identified intervals
        """
        return self.intervals


class IntervalIdentificationByHeartRate(object):
    """
    Class for identifying intervals based on heart rate.\n
    Args:
        distances (list):
            list of cummulative distances
        timestamps (list):
            list of timestamps
        altitudes (list):
            list of altitudes
        heart_rates (list):
            list of heart rates
        minimum_time (int):
            minimum time of an interval given in seconds
    """

    def __init__(
        self,
        distances: list,
        timestamps: list,
        altitudes: list,
        heart_rates: list,
        minimum_time: int = 30,
    ) -> None:
        """
        Initialisation method for IntervalIdentificationByHeartRate class.\n
        Args:
        distances (list):
            list of cummulative distances
        timestamps (list):
            list of timestamps
        altitudes (list):
            list of altitudes
        heart_rates (list):
            list of heart rates
        minimum_time (int):
            minimum time of an interval given in seconds
        """
        self.distances = distances
        self.timestamps = timestamps
        self.altitudes = altitudes
        self.heart_rates = heart_rates
        self.minimum_time = minimum_time

    def identify_intervals(self) -> None:
        """
        Method for identifying intervals from given data.
        """
        self.intervals = []
        sum_heartrate = 0

        # Calculating the sum and searching for None values
        i = 0
        while i < len(self.heart_rates):
            # If the value is number, it is added to sum
            if isinstance(self.heart_rates[i], int) or isinstance(
                self.heart_rates[i], numpy.int32
            ):
                sum_heartrate += self.heart_rates[i]
            else:
                j = i + 1
                while True:
                    if isinstance(self.heart_rates[j], int) or isinstance(
                        self.heart_rates[j], numpy.int32
                    ):
                        # If more than 10 seconds pass without a heart
                        # rate, the intervals cannot be identified
                        if (
                            self.timestamps[j] - self.timestamps[i - 1]
                        ).total_seconds() > 10:
                            raise ValueError(
                                "Input heart rates are not complete,",
                                "thus intervals cannot be identified.",
                            )
                        else:
                            sum_heartrate += (
                                self.heart_rates[j]
                                + self.heart_rates[i - 1] / 2
                            )
                            i = j - 1
                            break
                    else:
                        j += 1
            i += 1

        try:
            average_heartrate = sum_heartrate / len(
                self.heart_rates
            )  # Calculating the average heartrate
        except Exception:
            return

        # Identifying the intervals by heart rate
        # An interval is identified, when a segment's heart
        # rate is greater than the average heart rate
        interval = []
        for i in range(len(self.heart_rates)):
            # If the heart rate at i is greater than the average
            # heart rate, it belongs to an interval
            if (
                isinstance(self.heart_rates[i], int)
                or isinstance(self.heart_rates[i], numpy.int32)
            ) and self.heart_rates[i] > average_heartrate:
                interval.append(i)
            else:
                if interval:
                    self.intervals.append(copy.deepcopy(interval))
                    interval.clear()

        # Combining intervals according to the heart rate between them
        i = 1
        number_of_intervals = len(self.intervals) - 1
        while i < number_of_intervals:
            last_element = self.intervals[i - 1][
                -1
            ]  # Retrieving the last index in the previous interval
            first_element = self.intervals[i][
                0
            ]  # Retrieving the first index in the current interval
            average_heartrate_between = 0

            try:
                average_heartrate_between = sum(
                    self.heart_rates[last_element + 1: first_element]
                ) / len(
                    self.heart_rates[last_element + 1: first_element]
                )  # Calculating the average heart rate between two intervals
            except Exception:
                pass

            # If average heart rate between two intervals is less than 10,
            # the two intervals are combined
            if average_heartrate - average_heartrate_between < 10:
                # Indexes between the two intervals
                # have to be added to an interval
                self.intervals[i - 1].extend(
                    list(range(last_element + 1, first_element))
                )
                self.intervals[i - 1].extend(
                    self.intervals[i]
                )  # Current interval is added to the previous one
                self.intervals.remove(
                    self.intervals[i]
                )  # Current interval is removed from the list
                number_of_intervals -= 1
            else:
                i += 1

        # Removing intervals that are too short
        # (shorter than minimum_time, given as an argument)
        i = 0
        number_of_intervals = len(self.intervals) - 1
        while i < number_of_intervals:
            first_element = self.intervals[i][0]  # Retrieving the first index
            last_element = self.intervals[i][-1]  # Retrieving the last index

            # If an interval is shorter than self.minimum_time
            # seconds, it is removed
            if (
                self.timestamps[last_element] - self.timestamps[first_element]
            ).total_seconds() < self.minimum_time:
                self.intervals.remove(
                    self.intervals[i]
                )  # Current interval is removed from the list
                number_of_intervals -= 1
            else:
                i += 1

    def calculate_interval_statistics(self) -> dict:
        """
        Method for calculating interval statistics.\n
        Returns:
            data = {
                'number_of_intervals': number_of_intervals,
                'min_duration_interval': min_duration_interval,
                'max_duration_interval': max_duration_interval,
                'avg_duration_interval': avg_duration_interval,
                'min_distance_interval': min_distance_interval,
                'max_distance_interval': max_distance_interval,
                'avg_distance_interval': avg_distance_interval,
                'min_heartrate_interval': min_heartrate_interval,
                'max_heartrate_interval': max_heartrate_interval,
                'avg_heartrate_interval': avg_heartrate_interval,
            }
        """
        number_of_intervals = len(self.intervals)  # Number of intervals

        list_duration = []
        for item in self.intervals:
            list_duration.append(
                self.timestamps[item[-1]].timestamp()
                + self.timestamps[item[0]].timestamp()
            )

        if not list_duration:
            return

        list_duration = [
            (
                self.timestamps[item[-1]] - self.timestamps[item[0]]
            ).total_seconds()
            for item in self.intervals
        ]  # Time of every interval in list
        min_duration_interval = min(list_duration)
        max_duration_interval = max(list_duration)
        avg_duration_interval = sum(list_duration) / len(
            list_duration
        )  # Average duration of an interval

        list_distance = [
            self.distances[item[-1]] - self.distances[item[0]]
            for item in self.intervals
        ]  # Distance of every interval in list
        min_distance_interval = min(list_distance)
        max_distance_interval = max(list_distance)
        avg_distance_interval = sum(list_distance) / len(
            list_distance
        )  # Average distance of an interval

        list_heartrate = [
            sum(self.heart_rates[item[0]: item[-1] + 1])
            / len(self.heart_rates[item[0]: item[-1] + 1])
            for item in self.intervals
        ]  # Heart rate of every interval in list
        min_heartrate_interval = min(
            list_heartrate
        )  # Minimum heart rate of an interval
        max_heartrate_interval = max(
            list_heartrate
        )  # Maximum heart rate of an interval
        avg_heartrate_interval = sum(list_heartrate) / len(
            list_heartrate
        )  # Average heart rate of an interval

        # Building a dictionary
        data = {
            "number_of_intervals": number_of_intervals,
            "min_duration_interval": min_duration_interval,
            "max_duration_interval": max_duration_interval,
            "avg_duration_interval": avg_duration_interval,
            "min_distance_interval": min_distance_interval,
            "max_distance_interval": max_distance_interval,
            "avg_distance_interval": avg_distance_interval,
            "min_heartrate_interval": min_heartrate_interval,
            "max_heartrate_interval": max_heartrate_interval,
            "avg_heartrate_interval": avg_heartrate_interval,
        }

        return data

    def return_intervals(self) -> list:
        """
        Method for retrieving identified intervals.\n
        Returns:
            list: identified intervals
        """
        return self.intervals
