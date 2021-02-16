class IntervalIdentification(object):

    # To identify intervals, distances, timestamps, altitudes and threshold are needed
    def __init__(self, distances, timestamps, altitudes, threshold):
        self.distances = distances
        self.timestamps = timestamps
        self.altitudes = altitudes
        self.threshold = threshold  # Threshold should be given in percent (for example 30 % greater strength than average)

    # Identifying intervals from given data
    def identify_intervals(self):
        intervals = []
        average_power = 0.0

        # Loop to go through all segments and to identify intervals
        for i in range(1, len(self.distances)):
            time = self.timestamps[i] - self.timestamps[i - 1]  # Calculating time between two measures

    # Returning all found intervals
    def return_intervals(self):
        raise NotImplementedError