from sport_activities_features.tcx_manipulation import TCXFile


class SportyDataGen(object):
    """
    Class that contains selected and modified SportyDataGen methods for generation of sports activity collections.\n
    Args:
        **kwargs: various arguments
    Note:
        [WIP] This class is still under developement, therefore its methods may not work as expected.
    """
    def __init__(self, **kwargs) -> None:
        """
        Initialisation method for SportyDataGen class.\n
        Args:
            **kwargs: various arguments
        """
        self._set_parameters(**kwargs)

    def _set_parameters(self, **kwargs) -> None:
        """
        Method for setting parameters of the instance.\n
        Args:
            **kwargs: various arguments
        """
        return None

    def random_generation_without_clustering(self, activities) -> None:
        """
        Method for the random generation of sport activities (without clustering).\n
        Args:
            activities: 
        Note:
            Select n activities randomly without any special preprocessing tasks.
        """
        return None