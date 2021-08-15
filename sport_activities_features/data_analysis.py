from niaaml.data import CSVDataReader
from niaaml import PipelineOptimizer, Pipeline


class DataAnalysis(object):
    r"""Data analysis toolbox that uses automated machine learning to analyze extracted sport features.

    Date:
        2021

    Author:
        Luka Pečnik

    License:
        MIT

    Attributes:
        None
    """

    def __init__(self, **kwargs):
        r"""Initialize instance."""
        self._set_parameters(**kwargs)

    def _set_parameters(self, **kwargs):
        r"""Set parameters of the instance."""
        return None

    def analyze_data(
        self,
        src,
        fitness_name,
        population_size,
        number_of_evaluations,
        optimization_algorithm,
        classifiers,
        feature_selection_algorithms=None,
        feature_transform_algorithms=None,
        imputer=None,
    ):
        r"""Run AutoML process using NiaAML PipelineOptimizer class instance.

        Note:
            See NiaAML's documentation for more details on possible input parameters' values and further usage of the returned Pipeline object.

        Arguments:
            src (string): Path to a CSV file.
            fitness_name (str): Name of the fitness class to use as a function.
            population_size (uint): Number of individuals in the optimization process.
            number_of_evaluations (uint): Number of maximum evaluations.
            optimization_algorithm (str): Name of the optimization algorithm to use.
            classifiers (Iterable[Classifier]): Array of names of possible classifiers.
            feature_selection_algorithms (Optional[Iterable[str]]): Array of names of possible feature selection algorithms.
            feature_transform_algorithms (Optional[Iterable[str]]): Array of names of possible feature transform algorithms.
            imputer (Optional[str]): Name of the imputer used for features that contain missing values.

        Returns:
            Pipeline: Instance of Pipeline object from the NiaAML framework.
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
            fitness_name, population_size, number_of_evaluations, optimization_algorithm
        )
        return pipeline

    @staticmethod
    def load_pipeline(file_name):
        r"""Load a NiaAML's pipeline from a binary file.

        Note:
            See NiaAML's documentation for more details on the use of the Pipeline class.

        Arguments:
            file_name (string): Path to a binary pipeline file.
        """
        return Pipeline.load(file_name)
