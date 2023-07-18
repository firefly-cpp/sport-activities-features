import numpy


class FileManipulation:

    """Superclass of GPXFile and TCXFile. Contains common
    methods of both classes, that have the same implementation.
    e.g. (filling missing values).
    """

    def count_missing_values(self, list):
        """Counts the number of elements with value Nona.

        Args:
        ----
            list (list/ndarray): list to check
        Returns:
            (int): number of elements with value None in list.
        """
        count = 0
        for i in list:
            if i is None:
                count += 1
        return count

    def __missing_from_to(self, lst, start):
        """Finds to which index the values are missing
        Args:
            lst (list/ndarray): list on which to search
            for consecutive missing values
            start(int): index from where to search forward
        Returns:
            (int): ending index of consecutive missing values.
        """
        index = start
        while index < len(lst):
            if lst[index] is None:
                index += 1
            else:
                break
        return index

    def __set_value_type(self, baseline, value):
        """Private method that changes the value into
        baseline type (chooses between int and float).

        Args:
        ----
            baseline: who to compare to
            value: who to compare
        Returns:
            value transformed in the same type as baseline.

        """
        if (
            isinstance(baseline, int | numpy.int32 | numpy.int64)
        ):
            return round(value)
        if isinstance(baseline, float):
            return float(value)
        return None

    def linear_fill_missing_values(self, activity, key, max_seconds=15):
        """Function that lineary fills missing values, if the
        successive missing values are up to (max_seconds) apart.

        Args:
        ----
            activity: TCXReader read file
            key (str): dictionary key (e.g. 'heartrates', 'distances', ...)
            max_seconds (int): maximum time between two valid values,
            to still fill the missing values.

        Returns:
        -------
            / Transforms the sent array / list.
        """
        index = 0
        count = len(activity[key])
        while index < count:
            if activity[key][index] is None:
                to = self.__missing_from_to(activity[key], index)
                if to + 1 < len(activity[key]):
                    time_between = (
                        activity['timestamps'][to]
                        - activity['timestamps'][index]
                    ).total_seconds()
                    if (
                        to + 1 < count
                        and index - 1 > 0
                        and time_between <= max_seconds
                    ):
                        starting_value = activity[key][index - 1]
                        ending_value = activity[key][to]
                        denominator = (to + 1) - (index - 1) - 1
                        numerator = 1
                        id = 0
                        for _i in activity[key][index:to]:
                            value = None
                            try:
                                value = starting_value * (
                                    (denominator - numerator) / denominator
                                ) + ending_value * (numerator / denominator)
                                value = self.__set_value_type(
                                    activity[key][index - 1], value,
                                )
                            except Exception as e:
                                print(str(e))
                            activity[key][index + id] = value
                            numerator += 1
                            id += 1
                index = to
            index += 1
