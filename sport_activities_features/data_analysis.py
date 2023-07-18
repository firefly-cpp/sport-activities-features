from collections.abc import Iterable

from numpy import uint

try:
    from niaaml import Pipeline, PipelineOptimizer
    from niaaml.data import CSVDataReader
except BaseException:
    pass


class DataAnalysis:

    """Class for data analysis that uses automated machine
    learning to analyze extracted sport features.\n
    Args:
        **kwargs:
            various arguments.
    """

    def __init__(self, **kwargs) -> None:
        """Initialisation method for DataAnalysis class.\n
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

    def analyze_data(
        self,
        src: str,
        fitness_name: str,
        population_size: uint,
        number_of_evaluations: uint,
        optimization_algorithm: str,
        classifiers: Iterable,
        feature_selection_algorithms: Iterable = None,
        feature_transform_algorithms: Iterable = None,
        imputer: str = None,
    ) -> Pipeline:
        """Method for running AutoML process using NiaAML
        PipelineOptimizer class instance.\n
        Args:
            src (str):
                path to a CSV file
            fitness_name (str):
                name of the fitness class to use as a function
            population_size (uint):
                number of individuals in the optimization process
            number_of_evaluations (uint):
                number of maximum evaluations
            optimization_algorithm (str):
                name of the optimization algorithm to use
            classifiers (Iterable[Classifier]):
                array of names of possible classifiers
            feature_selection_algorithms (Optional[Iterable[str]]):
                array of names of possible feature selection algorithms
            feature_transform_algorithms (Optional[Iterable[str]]):
                array of names of possible feature transform algorithms
            imputer (Optional[str]):
                name of the imputer used for features
                that contain missing values
        Returns:
            Pipeline: instance of Pipeline object from the NiaAML framework
        Note:
            See NiaAML's documentation for more details on possible
            input parameters' values and further usage of the
            returned Pipeline object.
        """
        data = CSVDataReader(src=src, contains_classes=True, has_header=True)
        pipeline_optimizer = PipelineOptimizer(
            data=data,
            classifiers=classifiers,
            feature_selection_algorithms=feature_selection_algorithms,
            feature_transform_algorithms=feature_transform_algorithms,
            imputer=imputer,
        )
        pipeline = pipeline_optimizer.run_v1(
            fitness_name,
            population_size,
            number_of_evaluations,
            optimization_algorithm,
        )
        return pipeline

    @staticmethod
    def load_pipeline(file_name: str) -> Pipeline:
        """Method for loading a NiaAML's pipeline from a binary file.\n
        Args:
            file_name (str):
                path to a binary pipeline file
        Note:
            See NiaAML's documentation for more details
            on the use of the Pipeline class.
        """
        return Pipeline.load(file_name)
