import math
import numbers

# Two power intervals closer than this (in seconds) are merged.
POWER_MERGE_GAP = 30
# Two heart rate intervals are merged if the gap between them is at most
# HEART_RATE_MERGE_GAP seconds and the average heart rate in the gap is
# less than HEART_RATE_MERGE_DIFFERENCE beats per minute below the overall
# average.
HEART_RATE_MERGE_GAP = 120
HEART_RATE_MERGE_DIFFERENCE = 10
# A gap without heart rate data of at most this many seconds (a short
# sensor dropout) does not split an interval; a longer one does.
HEART_RATE_MAX_MISSING = 10


def _is_number(value) -> bool:
    """True for int/float values, including numpy numbers, but not for
    None, bool or NaN."""
    return (
        isinstance(value, numbers.Real)
        and not isinstance(value, bool)
        and not math.isnan(value)
    )


def _runs(flags: list) -> list:
    """Return the runs of consecutive True values as lists of indexes,
    including a run that lasts until the end."""
    runs = []
    current = []
    for index, flag in enumerate(flags):
        if flag:
            current.append(index)
        elif current:
            runs.append(current)
            current = []
    if current:
        runs.append(current)
    return runs


def _merge(intervals: list, should_merge) -> list:
    """Merge neighbouring intervals while should_merge(previous, current)
    is True; the indexes between them become part of the interval."""
    merged = []
    for interval in intervals:
        if merged and should_merge(merged[-1], interval):
            previous = merged[-1]
            previous.extend(range(previous[-1] + 1, interval[0]))
            previous.extend(interval)
        else:
            merged.append(list(interval))
    return merged


def _remove_short(intervals: list, timestamps: list, minimum_time) -> list:
    """Remove intervals shorter than minimum_time seconds."""
    return [
        interval for interval in intervals
        if (
            timestamps[interval[-1]] - timestamps[interval[0]]
        ).total_seconds() >= minimum_time
    ]


def _summary(values: list) -> tuple:
    """(minimum, maximum, average) of the values, or Nones if empty."""
    if not values:
        return None, None, None
    return min(values), max(values), sum(values) / len(values)


class IntervalIdentificationByPower(object):
    """
    Class for identifying intervals based on power.\n
    Args:
        distances (list):
            list of cumulative distances
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
                list of cumulative distances
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
        Method for identifying intervals from given data.\n
        After the call, self.powers holds the estimated power (in W) of
        every segment between two consecutive points. Segments with a
        missing altitude are treated as flat; segments with a missing
        distance or time get power 0.
        """
        self.intervals = []
        powers = []
        power_sum = 0.0

        # Loop to go through all segments and to calculate the average power
        for i in range(1, len(self.distances)):
            # Without distance or time the power cannot be estimated,
            # the segment gets power 0
            if not (
                _is_number(self.distances[i])
                and _is_number(self.distances[i - 1])
                and self.timestamps[i] is not None
                and self.timestamps[i - 1] is not None
            ):
                powers.append(0)
                continue

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

            # Calculating the change of altitude between two measures;
            # without altitudes the segment is treated as flat
            if _is_number(self.altitudes[i]) and _is_number(
                self.altitudes[i - 1],
            ):
                altitude_change = self.altitudes[i] - self.altitudes[i - 1]
            else:
                altitude_change = 0.0

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

        # Calculation of the average power over all segments
        average_power = power_sum / len(powers) if powers else 0.0

        # Identifying the intervals by power
        # An interval is identified, when a segment's
        # power is greater than the average power
        intervals = _runs([power > average_power for power in powers])

        # Combining intervals that are less than POWER_MERGE_GAP seconds
        # apart. Combining according to power can be very problematic,
        # since there is no good way of knowing when two or more
        # intervals could be merged into a common interval
        def close_enough(previous: list, current: list) -> bool:
            gap = (
                self.timestamps[current[0]] - self.timestamps[previous[-1]]
            ).total_seconds()
            return gap < POWER_MERGE_GAP

        intervals = _merge(intervals, close_enough)

        # Removing intervals that are too short
        # (shorter than minimum_time, given as an argument)
        self.intervals = _remove_short(
            intervals, self.timestamps, self.minimum_time,
        )
        # Estimated power of every segment (point i to point i + 1) in W
        self.powers = powers

    def calculate_interval_statistics(self) -> dict:
        """
        Method for calculating interval statistics.\n
        Returns:
            dict: 
            {
                'number_of_intervals': number_of_intervals,
                'min_duration': min_duration_interval,
                'max_duration': max_duration_interval,
                'avg_duration': avg_duration_interval,
                'min_distance': min_distance_interval,
                'max_distance': max_distance_interval,
                'avg_distance': avg_distance_interval,
            }
        If no intervals were identified, number_of_intervals is 0 and the
        other values are None.
        """
        list_duration = [
            (
                self.timestamps[item[-1]] - self.timestamps[item[0]]
            ).total_seconds()
            for item in self.intervals
        ]  # Duration of every interval in seconds
        list_distance = [
            self.distances[item[-1]] - self.distances[item[0]]
            for item in self.intervals
        ]  # Distance of every interval

        min_duration, max_duration, avg_duration = _summary(list_duration)
        min_distance, max_distance, avg_distance = _summary(list_distance)

        return {
            'number_of_intervals': len(self.intervals),
            'min_duration': min_duration,
            'max_duration': max_duration,
            'avg_duration': avg_duration,
            'min_distance': min_distance,
            'max_distance': max_distance,
            'avg_distance': avg_distance,
        }

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
            list of cumulative distances
        timestamps (list):
            list of timestamps
        altitudes (list):
            list of altitudes
        heart_rates (list):
            list of heart rates
        minimum_time (int):
            minimum time of an interval given in seconds
        max_merge_gap (float):
            two intervals with a lower heart rate between them are merged
            only if the gap is at most this many seconds
        max_missing_gap (float):
            a gap without heart rate of at most this many seconds does not
            split an interval
    """

    def __init__(
        self,
        distances: list,
        timestamps: list,
        altitudes: list,
        heart_rates: list,
        minimum_time: int = 30,
        max_merge_gap: float = HEART_RATE_MERGE_GAP,
        max_missing_gap: float = HEART_RATE_MAX_MISSING,
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
        max_merge_gap (float):
            two intervals with a lower heart rate between them are merged
            only if the gap is at most this many seconds
        max_missing_gap (float):
            a gap without heart rate of at most this many seconds does not
            split an interval
        """
        self.distances = distances
        self.timestamps = timestamps
        self.altitudes = altitudes
        self.heart_rates = heart_rates
        self.minimum_time = minimum_time
        self.max_merge_gap = max_merge_gap
        self.max_missing_gap = max_missing_gap

    def identify_intervals(self) -> None:
        """
        Method for identifying intervals from given data.\n
        An interval is a run of points whose heart rate is above the
        average heart rate of the activity. Two neighbouring intervals are
        merged if
        - the gap between them has no heart rate data and lasts at most
          max_missing_gap seconds (a short sensor dropout), or
        - the gap lasts at most max_merge_gap seconds and its average
          heart rate is less than HEART_RATE_MERGE_DIFFERENCE below the
          overall average.\n
        Points without heart rate never belong to an interval, so a longer
        dropout splits an interval. Intervals shorter than minimum_time
        are removed. Without any heart rate data there are no intervals.
        """
        self.intervals = []

        recorded = [hr for hr in self.heart_rates if _is_number(hr)]
        if not recorded:
            return
        average_heartrate = sum(recorded) / len(recorded)

        # Identifying the intervals by heart rate
        # An interval is identified, when a segment's heart
        # rate is greater than the average heart rate
        intervals = _runs([
            _is_number(hr) and hr > average_heartrate
            for hr in self.heart_rates
        ])

        def should_merge(previous: list, current: list) -> bool:
            gap = (
                self.timestamps[current[0]] - self.timestamps[previous[-1]]
            ).total_seconds()
            between = [
                hr for hr in self.heart_rates[previous[-1] + 1: current[0]]
                if _is_number(hr)
            ]
            if not between:
                return gap <= self.max_missing_gap
            if gap > self.max_merge_gap:
                return False
            average_between = sum(between) / len(between)
            return (
                average_heartrate - average_between
                < HEART_RATE_MERGE_DIFFERENCE
            )

        intervals = _merge(intervals, should_merge)

        # Removing intervals that are too short
        # (shorter than minimum_time, given as an argument)
        self.intervals = _remove_short(
            intervals, self.timestamps, self.minimum_time,
        )

    def calculate_interval_statistics(self) -> dict:
        """
        Method for calculating interval statistics.\n
        Returns:
            dict:
            {
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
        If no intervals were identified, number_of_intervals is 0 and the
        other values are None.
        """
        list_duration = [
            (
                self.timestamps[item[-1]] - self.timestamps[item[0]]
            ).total_seconds()
            for item in self.intervals
        ]  # Duration of every interval in seconds
        list_distance = [
            self.distances[item[-1]] - self.distances[item[0]]
            for item in self.intervals
        ]  # Distance of every interval
        list_heartrate = []  # Average heart rate of every interval
        for item in self.intervals:
            recorded = [
                hr for hr in self.heart_rates[item[0]: item[-1] + 1]
                if _is_number(hr)
            ]
            if recorded:
                list_heartrate.append(sum(recorded) / len(recorded))

        min_duration, max_duration, avg_duration = _summary(list_duration)
        min_distance, max_distance, avg_distance = _summary(list_distance)
        min_heartrate, max_heartrate, avg_heartrate = _summary(list_heartrate)

        return {
            'number_of_intervals': len(self.intervals),
            'min_duration_interval': min_duration,
            'max_duration_interval': max_duration,
            'avg_duration_interval': avg_duration,
            'min_distance_interval': min_distance,
            'max_distance_interval': max_distance,
            'avg_distance_interval': avg_distance,
            'min_heartrate_interval': min_heartrate,
            'max_heartrate_interval': max_heartrate,
            'avg_heartrate_interval': avg_heartrate,
        }

    def return_intervals(self) -> list:
        """
        Method for retrieving identified intervals.\n
        Returns:
            list: identified intervals
        """
        return self.intervals
