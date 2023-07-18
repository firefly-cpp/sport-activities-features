class SportyDataGen:

    """Class that contains selected and modified SportyDataGen methods
    for generation of sports activity collections.\n
    Args:
        **kwargs: various arguments
    Reference:
        Fister Jr., I.,
        Vrbančič, G.,
        Brezočnik, L.,
        Podgorelec, V.,
        & Fister, I. (2018).
        SportyDataGen: An Online Generator of Endurance
                       Sports Activity Collections.
        In Central European Conference on Information
        and Intelligent Systems (pp. 171-178).
        Faculty of Organization and Informatics Varazdin.
    Reference URL:
        http://www.iztok-jr-fister.eu/static/publications/225.pdf
    Note:
        [WIP]
        This class is still under developement,
        therefore its methods may not work as expected.
    """

    def __init__(self, **kwargs) -> None:
        """Initialisation method for SportyDataGen class.\n
        Args:
            **kwargs:
                various arguments.
        """
        self._set_parameters(**kwargs)

    def _set_parameters(self, **kwargs) -> None:
        """Method for setting parameters of the instance.\n
        Args:
            **kwargs:
                various arguments.
        """
        return

    def random_generation_without_clustering(self, activities) -> None:
        """Method for the random generation of
        sport activities (without clustering).\n
        Args:
            activities:

        Note:
        ----
            Select n activities randomly without
            any special preprocessing tasks.
        """
        return
