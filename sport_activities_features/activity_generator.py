from sport_activities_features.tcx_manipulation import TCXFile


class SportyDataGen(object):
    r"""Implementation of selected and modified SportyDataGen methods for generation of sports activity collections.

    Date:
        2021

    License:
        MIT

    Reference: Fister Jr., I., Vrbančič, G., Brezočnik, L., Podgorelec, V., & Fister, I. (2018). SportyDataGen: An Online Generator of Endurance Sports Activity Collections. In Central European Conference on Information and Intelligent Systems (pp. 171-178). Faculty of Organization and Informatics Varazdin.

    Reference URL: http://www.iztok-jr-fister.eu/static/publications/225.pdf
    """

    def __init__(self, **kwargs):
        r"""Initialize instance."""
        self._set_parameters(**kwargs)

    def _set_parameters(self, **kwargs):
        r"""Set parameters of the instance."""
        return None

    def random_generation_without_clustering(self, activities):
        r"""Random generation of sport activities (without clustering).

        Note:
            Select n activities randomly without any special preprocessing tasks.

        """
        return 1
