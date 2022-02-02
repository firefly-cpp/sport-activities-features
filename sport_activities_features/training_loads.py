class BanisterTRIMP(object):
    """
    Class for calculation of Banisters TRIMP.\n
    Args:
        duration (float): total duration in minutes
        avg_hr (float): average heart rate in bpm
    """
    def __init__(self, duration: float, avg_hr: float) -> None:
        """
        Initialisation method for BanisterTRIMP class.\n
        Args:
            duration (float): total duration in minutes
            avg_hr (float): average heart rate in bpm
        """
        self.duration = duration
        self.avg_hr = avg_hr

    def calculate_TRIMP(self) -> float:
        """
        Method for the calculation of TRIMP.\n
        Returns:
            float: TRIMP value
        """
        return self.duration * self.avg_hr