from datetime import timedelta

import numpy as np
from tcxreader.tcxreader import TCXExercise


def _power_in_window(
    tcx: TCXExercise, window_size: float, offset: float,
) -> list:
    """Power values (W) of the trackpoints between start + offset and
    start + offset + window_size seconds, where start is the time of the
    first trackpoint with power. Trackpoints without power data (or with
    zero power) are skipped; an activity without power data gives [].
    """
    points = []
    for trackpoint in tcx.trackpoints:
        extensions = trackpoint.tpx_ext or {}
        watts = extensions.get('Watts')
        if watts is not None and watts > 0 and trackpoint.time is not None:
            points.append((trackpoint.time, watts))
    if not points:
        return []

    start_time = points[0][0] + timedelta(seconds=float(offset))
    end_time = start_time + timedelta(seconds=float(window_size))
    return [power for time, power in points if start_time <= time <= end_time]


class TrainingMetrics():
    r"""Class for TrainingMetrics.
    
    Reference paper:
        Allen, H., & Coggan, A. R. (2019). Training and racing with a power meter: Third edition (3rd ed.). Boulder, CO: VeloPress.
    """
    def __init__(self) -> None:        
        return
    
    def prepare_functional_threshold_power_data(self, tcx: TCXExercise, window_size: float = 30, offset: float = 0) -> float:
        """Method for extracting average power from trackpoints.\n
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
        """Method for calculating functional threshold power (FTP).\n
        Args:
            avg_watts (float):
                average value of watts/power during a test / training session [W]            
        Returns:
            float: value of functional threshold power in watts [W].
        Function:
            .. math::
                FTP = Average Watts \\cdot 0.95
        """        
        ftp = (avg_watts*0.95)
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
        ftp = (avg_watts*0.95)/mass
        return float(round(ftp,2))
    
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
        
        
        
        
        

    