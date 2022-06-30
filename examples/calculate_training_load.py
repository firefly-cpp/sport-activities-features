from sport_activities_features.tcx_manipulation import TCXFile
from sport_activities_features.training_loads import (
    BanisterTRIMP,
    EdwardsTRIMP
)


# Reading a TCX file.
tcx_file = TCXFile()
activity = tcx_file.read_one_file('../datasets/15.tcx')
timestamps = activity['timestamps']
heart_rates = activity['heartrates']


# Calculating Banister TRIMP.
duration = (timestamps[-1] - timestamps[0]).seconds
average_heart_rate = sum(filter(None, heart_rates)) / len(heart_rates)
banister = BanisterTRIMP(duration, average_heart_rate)
banister_TRIMP = banister.calculate_TRIMP()
print('Banister TRIMP:', int(banister_TRIMP))

# Calculating Edwards TRIMP.
edwards = EdwardsTRIMP(heart_rates, timestamps, max_heart_rate=200)
edwards_TRIMP = edwards.calculate_TRIMP()
print('Edwards TRIMP: ', edwards_TRIMP)
