"""This class is used for calculation of training loads."""

import warnings
from enum import Enum

import numpy as np


class Gender(Enum):

    """
    Gender Enum for the BanisterTRIMPv2 class.\n
    - MALE
    - FEMALE
    """

    male = 1
    female = 2


class BanisterTRIMPv2:

    """Class for calculation of Banister's TRIMP (training impulse).\n
    TRIMP = duration [min] * dHR * a * e^(b * dHR), where
    dHR = (average HR - resting HR) / (maximum HR - resting HR),
    a = 0.64, b = 1.92 for men and a = 0.86, b = 1.67 for women.\n
    Reference papers:
        Banister, Eric W. "Modeling elite athletic performance."
        Physiological testing of elite athletes 347 (1991): 403-422.\n
        Morton, R. H., Fitz-Clarke, J. R., Banister, E. W. "Modeling human
        performance in running." Journal of Applied Physiology 69.3
        (1990): 1171-1177.\n
    Args:
        duration (float):
            total duration in seconds
        average_heart_rate (float):
            average heart rate during the exercise in beats per minute
        rest_heart_rate (float):
            resting heart rate of the athlete in beats per minute
            (measured at rest, not the lowest heart rate of the exercise)
        max_heart_rate (float):
            maximum heart rate of the athlete in beats per minute
        gender (Gender):
            gender of the athlete (default male)
        min_heart_rate (float):
            deprecated, use rest_heart_rate
    """

    COEFFICIENTS = {
        Gender.male: (0.64, 1.92),
        Gender.female: (0.86, 1.67),
    }

    def __init__(
        self: 'BanisterTRIMPv2',
        duration: float,
        average_heart_rate: float,
        rest_heart_rate: float = None,
        max_heart_rate: float = None,
        gender: Gender = Gender.male,
        *,
        min_heart_rate: float = None,
    ) -> None:
        """Initialize BanisterTRIMPv2 class."""
        if min_heart_rate is not None:
            if rest_heart_rate is not None:
                msg = 'Pass rest_heart_rate only (min_heart_rate is deprecated).'
                raise TypeError(msg)
            warnings.warn(
                'min_heart_rate is deprecated, use rest_heart_rate: '
                "Banister's TRIMP needs the athlete's resting heart rate, "
                'not the lowest heart rate of the exercise.',
                DeprecationWarning,
                stacklevel=2,
            )
            rest_heart_rate = min_heart_rate
        if rest_heart_rate is None or max_heart_rate is None:
            msg = 'rest_heart_rate and max_heart_rate are required.'
            raise TypeError(msg)
        if max_heart_rate <= rest_heart_rate:
            msg = 'max_heart_rate must be greater than rest_heart_rate.'
            raise ValueError(msg)

        self.duration = duration
        self.average_heart_rate = average_heart_rate
        self.rest_heart_rate = rest_heart_rate
        self.max_heart_rate = max_heart_rate
        self.gender = gender

    def calculate_delta_hr_ratio(self: 'BanisterTRIMPv2') -> float:
        """Calculate the heart rate reserve ratio (dHR).

        The ratio ranges from 0 at the resting heart rate to 1 at the
        maximum heart rate.

        Returns:
            float: delta heart rate ratio.
        """
        return (self.average_heart_rate - self.rest_heart_rate) / \
            (self.max_heart_rate - self.rest_heart_rate)

    def calculate_weighting_factor(
        self: 'BanisterTRIMPv2', delta_hr_ratio: float,
    ) -> float:
        """Calculate the weighting factor a * e^(b * dHR).\n
        Args:
            delta_hr_ratio (float):
                delta heart rate ratio.
        Returns:
            float: weighting factor (Y).
        """
        a, b = self.COEFFICIENTS[self.gender]
        return a * np.exp(b * delta_hr_ratio)

    def calculate_TRIMP(self: 'BanisterTRIMPv2') -> float:
        """Calculate TRIMP.

        Returns:
            float: Banister TRIMP value.
        """
        duration_minutes = self.duration / 60
        delta_hr_ratio = self.calculate_delta_hr_ratio()
        weighting_factor = self.calculate_weighting_factor(delta_hr_ratio)

        return float(duration_minutes * delta_hr_ratio * weighting_factor)


class EdwardsTRIMP:

    """Class for calculation of Edwards TRIMP.\n
    Reference paper:
        https://www.frontiersin.org/articles/10.3389/fphys.2020.00480/full\n
    Args:
        heart_rates (list):
            list of ints representing heart rates in beats per minute
        timestamps (list):
            list of timestamps
        max_heart_rate (int):
            maximum heart rate of an athlete.
    """

    def __init__(
        self,
        heart_rates: list,
        timestamps: list,
        max_heart_rate: int = 200,
    ) -> None:
        """Initialisation method for EdwardsTRIMP class.\n
        Args:
            heart_rates (list):
                list of ints representing heart rates in beats per minute
            timestamps (list):
                list of timestamps
            max_heart_rate (int):
                maximum heart rate of an athlete.
        """
        self.heart_rates = heart_rates
        self.timestamps = timestamps
        self.max_heart_rate = max_heart_rate

    def calculate_TRIMP(self) -> float:
        """Method for the calculation of the TRIMP.\n
        Returns:
            float: Edwards TRIMP value.
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

    """Class for calculation of Lucia's TRIMP.\n
    Reference:
        https://www.trainingimpulse.com/lucias-trimp-0\n
    Args:
        heart_rates (list):
            list of ints representing heart rates in beats per minute
        timestamps (list):
            list of timestamps
        VT1 (int):
            ventilatory threshold to divide the low and the moderate zone
        VT2 (int):
            ventilatory threshold to divide the moderate and the high zone.
    """

    def __init__(
        self,
        heart_rates: list,
        timestamps: list,
        VT1: int = 160,
        VT2: int = 180,
    ) -> None:
        """Initialisation method for LuciaTRIMP class.\n
        Args:
            heart_rates (list):
                list of ints representing heart rates in beats per minute
            timestamps (list):
                list of timestamps
            VT1 (int):
                ventilatory threshold to divide the low and the moderate zone
            VT2 (int):
                ventilatory threshold to divide the moderate and the high zone.
        """
        self.heart_rates = heart_rates
        self.timestamps = timestamps
        self.VT1 = VT1
        self.VT2 = VT2

    def calculate_TRIMP(self) -> float:
        """Method for the calculation of the TRIMP.\n
        Returns:
            float: Lucia's TRIMP value.
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
