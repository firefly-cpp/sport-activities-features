from tcxreader.tcxreader import TCXExercise
import numpy as np


class TrainingMetrics():
    """ Class for TrainingMetrics."""
    def __init__(self) -> None:        
        return
    
    def functional_threshold_power(self,avg_watts:float, mass:float) -> float:        
        """Method for calculating functional threshold power (FTP).\n
        Args:
            avg_watts (float):
                average value of watts/power during a test / training session [W]            
        Returns:
            float: value of functional threshold power in watts W.
        """        
        ftp = (avg_watts*0.95)
        return float(round(ftp,2))
    
    def prepare_normalized_power_data(self,tcx: TCXExercise, window_size=30) -> list:
        """Method for extracting timestamps and power from trackpoints.\n
        Args:
            tcx (TCXExercise):
                TCXExercise object which contains data for one session   
            window_size (int):
                number of seconds to use for sampling data
        Returns:
            power_data (list):
                list of power values within *window_size* seconds from the start time.
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
            start_time = np.datetime64(power_data[0]['time'])
            end_time = start_time + np.timedelta64(window_size, 's')
            power_data = [entry['power'] for entry in power_data if entry['time'] <= end_time]            
        
        return power_data
    
    def normalized_power(self, tcx: TCXExercise, window_size: int) -> float|None:        
        """Method for calculating normalized power (NP).\n
        Args:
            tcx (TCXExercise):
                TCXExercise object which contains data for one session
            window_size (int):
                number of seconds to use for sampling data
        Returns:
            float: value of normalized power [W].
        """
        power_data = self.prepare_normalized_power_data(tcx,window_size)
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
        return (normalized_power / ftp)
    
    def training_score_stress(self,duration:int, normalized_power:float, ftp:float) -> float:
        """Method for calculating training score stress (TSS).\n
        Args:
            duration (int):
                duration of an training session in seconds [s]
            normalized_power (float):
                value of normalized power from a training session in watts [W]
            ftp (float):
                value of functional threshold power in watts per kilogram [W/kg].                
        Returns:
            float: value of training score stress.
        """
        intensity_factor = self.calculate_intensity_factor(normalized_power,ftp)
        tss = ((duration * normalized_power * intensity_factor) / (ftp * 36))
        return float(round(tss,2))
        
        
        
        
        

    