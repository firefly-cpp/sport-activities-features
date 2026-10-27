"""This example presents how to calculate Banister,
Edwards and Lucia TRIMP (training impulse).
"""
from sport_activities_features import (
    BanisterTRIMPv2,
    EdwardsTRIMP,
    Gender,
    LuciaTRIMP,
    TCXFile,
)

# Reading a TCX file.
tcx_file = TCXFile()
tcx_exercise = tcx_file.read_one_file('../datasets/15.tcx')
activity = tcx_file.extract_activity_data(tcx_exercise)

timestamps = activity['timestamps']
heart_rates = activity['heartrates']

# Calculating Banister TRIMP.
# Resting and maximum heart rate are properties of the athlete
# (measured separately), not values taken from this activity.
duration = (timestamps[-1] - timestamps[0]).total_seconds()
recorded_heart_rates = [hr for hr in heart_rates if hr is not None]
average_heart_rate = sum(recorded_heart_rates) / len(recorded_heart_rates)
banister = BanisterTRIMPv2(duration=duration,
                           average_heart_rate=average_heart_rate,
                           rest_heart_rate=55,
                           max_heart_rate=190,
                           gender=Gender.male)
banister_TRIMP = banister.calculate_TRIMP()
print("Banister's TRIMP: ", round(banister_TRIMP, 1))

# Calculating Edwards TRIMP.
edwards = EdwardsTRIMP(heart_rates, timestamps, max_heart_rate=200)
edwards_TRIMP = edwards.calculate_TRIMP()
print('Edwards TRIMP: ', edwards_TRIMP)

# Calculating Lucia's TRIMP.
lucia = LuciaTRIMP(heart_rates, timestamps, VT1=160, VT2=180)
lucia_TRIMP = lucia.calculate_TRIMP()
print("Lucia's TRIMP: ", lucia_TRIMP)
