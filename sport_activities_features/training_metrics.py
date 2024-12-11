from tcxreader.tcxreader import TCXExercise
import numpy as np


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
                average value of watts/power during a test / training session [W]
        """
        trackpoints = tcx.trackpoints
        power_data = []
        for tpx in trackpoints:
            if tpx.tpx_ext['Watts'] is not None:
                if tpx.tpx_ext['Watts'] > 0:
                    power_data.append({
                        'time': tpx.time,
                        'power': tpx.tpx_ext['Watts']
                    })
        
        if power_data:
            start_time = np.datetime64(power_data[0]['time']) + np.timedelta64(int(offset), 's')
            end_time = start_time + np.timedelta64(window_size, 's')
            power_data = [entry['power'] for entry in power_data if start_time <= np.datetime64(entry['time']) <= end_time]
        
        avg_watts = np.mean(power_data) if power_data else 0
        return avg_watts
    
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
                list of power values within *window_size* seconds from the start time + offset.
        """
        trackpoints = tcx.trackpoints
        power_data: list = []
        for tpx in trackpoints:
            if tpx.tpx_ext['Watts'] is not None:
                if tpx.tpx_ext['Watts'] > 0:
                    power_data.append({
                        'time': tpx.time,
                        'power': tpx.tpx_ext['Watts']
                    })
        
        if power_data:
            start_time = np.datetime64(power_data[0]['time']) + np.timedelta64(int(offset), 's')
            end_time = start_time + np.timedelta64(window_size, 's')
            power_data = [entry['power'] for entry in power_data if start_time <= np.datetime64(entry['time']) <= end_time]
        
        return power_data
    
    def normalized_power(self, power_data: list, window_size: int) -> float:
        """Method for calculating normalized power (NP).\n
        Args:
            power_data (list):
                List of power values within *window_size* seconds from the start time + offset\n
                Use prepare_normalized_power_data method to get the data from a TCXExercise object.
            window_size (int):
                Number of trackpoints to use for sampling data
        Returns:
            float: value of normalized power [W].
        Function:            
            1. Calculate the rolling average of the power data.
            2. Calculate the fourth power of the values from the previous step.
            3. Calculate the average of the values from the previous step.
            4. Take the fourth root of the average from the previous step.
            
        """        
        try:
            # Step 1: Calculate the rolling average
            rolling_average = []
            for i in range(len(power_data) - window_size + 1):
                window = power_data[i:i + window_size]
                rolling_average.append(np.mean(window))
            
            rolling_average = np.array(rolling_average)
            
            # Step 2: Calculate the 4th power of the values from the previous step
            rolling_avg_powered = rolling_average ** 4
            
            # Step 3: Calculate the average of the values from the previous step
            avg_powered_values = np.mean(rolling_avg_powered)
            
            # Step 4: Take the fourth root of the average from the previous step
            normalized_power = avg_powered_values ** 0.25
            
            return round(normalized_power, 2)
        except:
            return None    
    
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
        
        
        
        
        

    