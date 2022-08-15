import numpy


class FileManipulation():
    """
    Superclass of GPXFile and TCXFile. Contains common methods of both classes, that have the same implementation.
    e.g. (filling missing values)
    """
    def __missing_from_to(self, lst, start):
        """
        Finds to which index the values are missing
        Args:
            lst (list/ndarray): list on which to search for consecutive missing values
            start(int): index from where to search forward
        Returns:
            (int): ending index of consecutive missing values
        """
        index = start
        while index < len(lst):
            if lst[index]==None:
                index+=1
            else:
                break
        return index

    def __set_value_type(self, baseline, value):
        """
        Private method that changes the value into baseline type (chooses between int and float)
        Args:
            baseline: who to compare to
            value: who to compare
        Returns:
            value transformed in the same type as baseline

        """
        if isinstance(baseline, int) \
                or isinstance(baseline, numpy.int32) \
                or isinstance(baseline, numpy.int64):
            return round(value)
        if isinstance(baseline, float):
            return float(value)

    def linear_fill_missing_values(self, activity, key, max_seconds=15):
        """
        Function that lineary fills missing values, if the successive missing values are up to (max_seconds) apart.
        Args:
            activity: TCXReader read file
            key (str): dictionary key (e.g. 'heartrates', 'distances', ...)
            max_seconds (int): maximum time between two valid values, to still fill the missing values

        Returns:
            / Transforms the sent array / list.
        """
        index = 0
        count = len(activity[key])
        while index<count:
            if activity[key][index] == None:
                to = self.__missing_from_to(activity[key], index)
                time_between = (activity['timestamps'][to]-activity['timestamps'][index]).total_seconds()
                if(to+1<count and index-1>0 and time_between<=max_seconds):
                    starting_value = activity[key][index-1]
                    ending_value = activity[key][to+1]
                    denominator = (to+1)-(index-1)
                    numerator = 1
                    id = 0
                    for i in activity[key][index:to]:
                        value = starting_value*((denominator-numerator)/denominator)+ending_value*(numerator/denominator)
                        value = self.__set_value_type(activity[key][index-1], value)
                        activity[key][index+id]=value
                        id+=1
                    index=to
            index+=1
