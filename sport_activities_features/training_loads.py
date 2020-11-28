class BanisterTRIMP(object):
    r"""Implementation of Banisters TRIMP

    Attributes:
                float: Total duration in minutes
                float: Average heart rate in bpm

        """

    def __init__(self, duration, avg_hr):
        self.duration = duration
        self.avg_hr = avg_hr

    def calculate_TRIMP(self):
        r"""Calculation of TRIMP

                Reference:
                        Banister, E. W. "Modeling elite athletic performance." Physiological testing of elite athletes 403 (1991): 424.

                Returns:
                        float: TRIMP value

                """
        return self.duration * self.avg_hr
