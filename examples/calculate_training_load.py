"""This example presents how to calculate Banister,
Edwards and Lucia TRIMP (training impulse).
"""
from sport_activities_features import (
    BanisterTRIMPv1,
    BanisterTRIMPv2,
    EdwardsTRIMP,
    LuciaTRIMP,
    TCXFile,
)

# Reading a TCX file.
tcx_file = TCXFile()
activity = tcx_file.read_one_file('../datasets/15.tcx')

timestamps = activity['timestamps']
heart_rates = activity['heartrates']

# Calculating simple Banister TRIMP.
duration = (timestamps[-1] - timestamps[0]).seconds
average_heart_rate = sum(filter(None, heart_rates)) / len(heart_rates)
banister_v1 = BanisterTRIMPv1(duration, average_heart_rate)
banister_TRIMP = banister_v1.calculate_TRIMP()
print("Banister's simple TRIMP:", int(banister_TRIMP))

# Calculating Banister TRIMP.
# Duration and average heart rate are the same as in the previous example.
min_heart_rate = min(filter(None, heart_rates))
max_heart_rate = max(filter(None, heart_rates))
banister_v2 = BanisterTRIMPv2(duration=duration,
                              average_heart_rate=average_heart_rate,
                              min_heart_rate=min_heart_rate,
                              max_heart_rate=max_heart_rate)
banister_TRIMPv2 = banister_v2.calculate_TRIMP()
print("Banister's TRIMP: ", str(banister_TRIMPv2))

# Calculating Edwards TRIMP.
edwards = EdwardsTRIMP(heart_rates, timestamps, max_heart_rate=200)
edwards_TRIMP = edwards.calculate_TRIMP()
print('Edwards TRIMP: ', edwards_TRIMP)

# Calculating Lucia's TRIMP.
lucia = LuciaTRIMP(heart_rates, timestamps, VT1=160, VT2=180)
lucia_TRIMP = lucia.calculate_TRIMP()
print("Lucia's TRIMP: ", lucia_TRIMP)
