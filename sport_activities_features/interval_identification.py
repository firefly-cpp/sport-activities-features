class IntervalIdentification(object):

    # To identify intervals, distances, timestamps, altitudes and threshold are needed
    def __init__(self, distances, timestamps, altitudes, threshold):
        self.distances = distances
        self.timestamps = timestamps
        self.altitudes = altitudes
        self.threshold = threshold

    # Method to return True if the segment is an interval, False otherwise
    def is_interval(self):
        raise NotImplementedError

    # Identifying intervals from given data
    def identify_intervals(self):
        raise NotImplementedError

    # Returning all found intervals
    def return_intervals(self):
        raise NotImplementedError