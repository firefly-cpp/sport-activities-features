import numpy as np


class BanisterTRIMP:
    """
    Class for calculation of Banister's TRIMP.\n
    Reference paper:
        Banister, Eric W. "Modeling elite athletic performance."
        Physiological testing of elite athletes 347 (1991): 403-422.\n
    Args:
        duration (float):
            total duration in seconds
        average_heart_rate (float):
            average heart rate in beats per minute
    """
    def __init__(self, duration: float, average_heart_rate: float) -> None:
        """
        Initialization method for BanisterTRIMP class.\n
        Args:
            duration (float):
                total duration in seconds
            average_heart_rate (float):
                average heart rate in beats per minute
        """
        self.duration = duration
        self.average_heart_rate = average_heart_rate

    def calculate_TRIMP(self) -> float:
        """
        Method for the calculation of the TRIMP.\n
        Returns:
            float: Banister TRIMP value
        """
        return self.duration * self.average_heart_rate


class EdwardsTRIMP:
    """
    Class for calculation of Edwards TRIMP.\n
    Reference paper:
        https://www.frontiersin.org/articles/10.3389/fphys.2020.00480/full\n
    Args:
        heart_rates (list[int]):
            list of heart rates in beats per minute
        timestamps (list[timestamp]):
            list of timestamps
        max_heart_rate (int):
            maximum heart rate of an athlete
    """
    def __init__(
        self,
        heart_rates: list,
        timestamps: list,
        max_heart_rate: int = 200
    ) -> None:
        """
        Initialization method for EdwardsTRIMP class.\n
        Args:
            heart_rates (list[int]):
                list of heart rates in beats per minute
            timestamps (list[timestamp]):
                list of timestamps
            max_heart_rate (int):
                maximum heart rate of an athlete
        """
        self.heart_rates = heart_rates
        self.timestamps = timestamps
        self.max_heart_rate = max_heart_rate

    def calculate_TRIMP(self) -> float:
        """
        Method for the calculation of the TRIMP.\n
        Returns:
            float: Edwards TRIMP value
        """
        TRIMP = 0

        # Loop for iterating through the heart rates and calculating the TRIMP.
        for i in np.arange(np.shape(self.heart_rates)[0] - 1):
            # If a current heart rate is NoneType or other non-integer
            # value, it is ignored in the calculation of the TRIMP.
            if not self.heart_rates[i]:
                continue

            # Duration between two timestamps should be given in seconds.
            duration = (self.timestamps[i + 1] - self.timestamps[i]).seconds

            # See the reference paper for more information
            # about the TRIMP calculation:
            # https://www.frontiersin.org/articles/10.3389/fphys.2020.00480/full
            if self.heart_rates[i] > 0.9 * self.max_heart_rate:
                TRIMP += 5 * duration
            elif self.heart_rates[i] > 0.8 * self.max_heart_rate:
                TRIMP += 4 * duration
            elif self.heart_rates[i] > 0.7 * self.max_heart_rate:
                TRIMP += 3 * duration
            elif self.heart_rates[i] > 0.6 * self.max_heart_rate:
                TRIMP += 2 * duration
            elif self.heart_rates[i] > 0.5 * self.max_heart_rate:
                TRIMP += 1 * duration

        return TRIMP


class LuciaTRIMP:
    """
    Class for calculation of Lucia's TRIMP.\n
    Reference:
        https://www.trainingimpulse.com/lucias-trimp-0\n
    Args:
        heart_rates (list[int]):
            list of heart rates in beats per minute
        timestamps (list[timestamp]):
            list of timestamps
        VT1 (int):
            ventilatory threshold to divide the low and the moderate zone
        VT2 (int):
            ventilatory threshold to divide the moderate and the high zone
    """
    def __init__(
        self,
        heart_rates: list,
        timestamps: list,
        VT1: int = 160,
        VT2: int = 180
    ) -> None:
        """
        Initialization method for LuciaTRIMP class.\n
        Args:
            heart_rates (list[int]):
                list of heart rates in beats per minute
            timestamps (list[timestamp]):
                list of timestamps
            VT1 (int):
                ventilatory threshold to divide the low and the moderate zone
            VT2 (int):
                ventilatory threshold to divide the moderate and the high zone
        """
        self.heart_rates = heart_rates
        self.timestamps = timestamps
        self.VT1 = VT1
        self.VT2 = VT2

    def calculate_TRIMP(self) -> float:
        """
        Method for the calculation of the TRIMP.\n
        Returns:
            float: Lucia's TRIMP value
        """
        TRIMP = 0

        # Loop for iterating through the heart rates and calculating the TRIMP.
        for i in np.arange(np.shape(self.heart_rates)[0] - 1):
            # If a current heart rate is NoneType or other non-integer
            # value, it is ignored in the calculation of the TRIMP.
            if not self.heart_rates[i]:
                continue

            # Duration between two timestamps should be given in seconds.
            duration = (self.timestamps[i + 1] - self.timestamps[i]).seconds

            # See the reference paper for more information
            # about the TRIMP calculation:
            # https://www.frontiersin.org/articles/10.3389/fphys.2020.00480/full
            if self.heart_rates[i] < self.VT1:
                TRIMP += 1 * duration
            elif self.heart_rates[i] < self.VT2:
                TRIMP += 2 * duration
            else:
                TRIMP += 3 * duration

        return TRIMP
