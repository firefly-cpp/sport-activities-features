from datetime import timedelta

import numpy as np
from tcxreader.tcxreader import TCXExercise


# Standard FTP estimate (Allen & Coggan): 95 % of the best average power
# over 20 minutes.
FTP_TEST_DURATION = 1200
FTP_FACTOR = 0.95
# A power sample holds until the next sample, but at most this many
# seconds; a longer gap (e.g. auto-pause) counts as 0 W.
MAX_POWER_HOLD = 10


def _power_points(tcx: TCXExercise) -> list:
    """(time, power in W) of all trackpoints that have power data,
    including 0 W (coasting), ordered by time."""
    points = []
    for trackpoint in tcx.trackpoints:
        extensions = trackpoint.tpx_ext or {}
        watts = extensions.get('Watts')
        if watts is not None and trackpoint.time is not None:
            points.append((trackpoint.time, watts))
    points.sort(key=lambda point: point[0])
    return points


def _power_per_second(points: list) -> np.ndarray:
    """Power resampled to one value per second from the first sample on.
    Each sample holds until the next one, at most MAX_POWER_HOLD seconds;
    seconds not covered count as 0 W."""
    first_time = points[0][0]
    starts = [
        int(round((time - first_time).total_seconds())) for time, _ in points
    ]
    series = np.zeros(starts[-1] + 1)
    for index, (start, (_, watts)) in enumerate(zip(starts, points)):
        following = starts[index + 1] if index + 1 < len(starts) else start + 1
        series[start:min(following, start + MAX_POWER_HOLD)] = watts
    return series


def _power_in_window(
    tcx: TCXExercise, window_size: float, offset: float,
) -> list:
    """Power values (W) of the trackpoints between start + offset and
    start + offset + window_size seconds, where start is the time of the
    first trackpoint with power above 0 W. Trackpoints without power data
    are skipped, 0 W values are kept; an activity without power data
    gives [].
    """
    points = _power_points(tcx)
    started = [time for time, watts in points if watts > 0]
    if not started:
        return []

    start_time = started[0] + timedelta(seconds=float(offset))
    end_time = start_time + timedelta(seconds=float(window_size))
    return [power for time, power in points if start_time <= time <= end_time]


class TrainingMetrics():
    r"""Class for TrainingMetrics.
    
    Reference paper:
        Allen, H., & Coggan, A. R. (2019). Training and racing with a power meter: Third edition (3rd ed.). Boulder, CO: VeloPress.
    """
    def __init__(self) -> None:        
        return
    
    def prepare_functional_threshold_power_data(self, tcx: TCXExercise, window_size: float = FTP_TEST_DURATION, offset: float = 0) -> float:
        """Method for extracting the average power of a test window.\n
        Use it for a structured FTP test: the window starts *offset* seconds
        after the first trackpoint with power and lasts *window_size* seconds
        (20 minutes by default). To find the best 20 minutes of any
        activity, use best_average_power or
        estimate_functional_threshold_power instead.\n
        Args:
            tcx (TCXExercise):
                TCXExercise object which contains data for one session
            window_size (float):
                number of seconds to use for sampling data [s]
            offset (float):
                number of seconds to skip from the start time [s]
        Returns:
            avg_watts (float):
                average value of watts/power during a test / training session [W];
                0 if the activity has no power data
        """
        power_data = _power_in_window(tcx, window_size, offset)
        return float(np.mean(power_data)) if power_data else 0

    def functional_threshold_power(self,avg_watts:float) -> float:        
        """Method for calculating functional threshold power (FTP) from the
        average power of a 20-minute test (see
        prepare_functional_threshold_power_data and best_average_power).\n
        Args:
            avg_watts (float):
                average power of a 20-minute test or best effort [W]
        Returns:
            float: value of functional threshold power in watts [W].
        Function:
            .. math::
                FTP = Average Watts \\cdot 0.95
        """        
        ftp = (avg_watts * FTP_FACTOR)
        return float(round(ftp,2))
    
    def functional_threshold_power_with_mass(self,avg_watts:float,mass:float) -> float:        
        """Method for calculating functional threshold power with mass (FTP).\n
        Args:
            avg_watts (float):
                average value of watts/power during a test / training session [W]            
            mass (float):
                value of an athlete's mass in kilograms [kg]
        Returns:
            float: value of functional threshold power in power to weight ratio [W/kg].
        Function:
            .. math::
                FTP = \\frac{Average Watts \\cdot 0.95}{Mass}
        
        """        
        ftp = (avg_watts * FTP_FACTOR) / mass
        return float(round(ftp,2))
    
    def best_average_power(self, tcx: TCXExercise, duration: float = FTP_TEST_DURATION) -> float:
        """Method for finding the best (highest) average power over any
        continuous *duration* seconds of an activity.\n
        Power is resampled to one value per second: every sample holds
        until the next one (at most MAX_POWER_HOLD seconds, a longer gap
        counts as 0 W). Zero power (coasting) is part of the average.\n
        Args:
            tcx (TCXExercise):
                TCXExercise object which contains data for one session
            duration (float):
                length of the window in seconds (default 20 minutes) [s]
        Returns:
            float: best average power [W]; None if the activity has no
            power data or is shorter than *duration*.
        """
        points = _power_points(tcx)
        window = int(round(duration))
        if not points or window < 1:
            return None
        series = _power_per_second(points)
        if len(series) < window:
            return None
        cumulative = np.concatenate([[0.0], np.cumsum(series)])
        averages = (cumulative[window:] - cumulative[:-window]) / window
        return float(round(averages.max(), 2))

    def estimate_functional_threshold_power(self, tcx: TCXExercise, duration: float = FTP_TEST_DURATION) -> float:
        """Method for estimating functional threshold power (FTP) from an
        activity, as 95 % of the best average power over 20 minutes
        (Allen & Coggan).\n
        Args:
            tcx (TCXExercise):
                TCXExercise object which contains data for one session
            duration (float):
                length of the best-effort window in seconds; the 0.95 factor
                applies to 20 minutes (the default)
        Returns:
            float: estimated FTP [W]; None if the activity has no power
            data or is shorter than *duration*.
        Function:
            .. math::
                FTP = 0.95 \\cdot P_{best\\ 20\\ min}
        """
        best = self.best_average_power(tcx, duration)
        if best is None:
            return None
        return self.functional_threshold_power(best)

    def prepare_normalized_power_data(self,tcx: TCXExercise, window_size:float = 30, offset: float = 0) -> list:
        """Method for extracting timestamps and power from trackpoints.\n
        Args:
            tcx (TCXExercise):
                TCXExercise object which contains data for one session   
            window_size (float):
                number of seconds to use for sampling data
            offset (float):
                number of seconds to skip from the start time
        Returns:
            power_data (list):
                list of power values within *window_size* seconds from the start time + offset;
                empty if the activity has no power data.
        """
        return _power_in_window(tcx, window_size, offset)

    def normalized_power(self, power_data: list, window_size: int) -> float:
        """Method for calculating normalized power (NP).\n
        Args:
            power_data (list):
                List of power values within *window_size* seconds from the start time + offset\n
                Use prepare_normalized_power_data method to get the data from a TCXExercise object.
            window_size (int):
                Number of trackpoints to use for sampling data
        Returns:
            float: value of normalized power [W]; None if there are fewer
            than *window_size* power values.
        Function:            
            1. Calculate the rolling average of the power data.
            2. Calculate the fourth power of the values from the previous step.
            3. Calculate the average of the values from the previous step.
            4. Take the fourth root of the average from the previous step.
            
        """        
        if window_size < 1 or len(power_data) < window_size:
            return None

        # Step 1: Calculate the rolling average
        rolling_average = np.convolve(
            np.asarray(power_data, dtype=float),
            np.ones(int(window_size)) / int(window_size),
            mode='valid',
        )

        # Step 2: Calculate the 4th power of the values from the previous step
        rolling_avg_powered = rolling_average ** 4

        # Step 3: Calculate the average of the values from the previous step
        avg_powered_values = np.mean(rolling_avg_powered)

        # Step 4: Take the fourth root of the average from the previous step
        normalized_power = avg_powered_values ** 0.25

        return round(float(normalized_power), 2)

    def calculate_intensity_factor(self, normalized_power: float, ftp: float) -> float:
        """Calculate the intensity factor of a training session.\n
        Args:
            normalized_power (float):
                The normalized power of the workout in watts. [W]
            ftp (float):
                The functional threshold power of the athlete in watts. [W]
        Returns:
            float: The intensity factor, which is the ratio of normalized power to FTP.        
        Function:
            .. math::
                IF = \\frac{NP}{FTP}
        
        """
        if ftp is None or ftp <= 0:
            msg = 'ftp must be a positive number of watts.'
            raise ValueError(msg)
        return (normalized_power / ftp)
    
    def training_stress_score(self,duration:int, normalized_power:float, ftp:float) -> float:
        """Method for calculating training stress score (TSS).\n
        Args:
            duration (int):
                duration of an training session in seconds [s]
            normalized_power (float):
                value of normalized power from a training session in watts [W]
            ftp (float):
                value of functional threshold power in watts [W].                
        Returns:
            float: value of training score stress.
        Function:
            .. math::
                TSS = \\frac{Duration \\cdot NP \\cdot IF}{FTP \\cdot 3600} \\cdot 100 = \\frac{Duration \\cdot NP \\cdot IF}{FTP \\cdot 36}
            
        """
        intensity_factor = self.calculate_intensity_factor(normalized_power,ftp)
        tss = ((duration * normalized_power * intensity_factor) / (ftp * 36))
        return float(round(tss,2))
        
        
        
        
        

    