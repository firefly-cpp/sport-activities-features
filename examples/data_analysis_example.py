"""This example presents how to use the DataAnalysis class
along with the NiaAML automated machine learning framework.
"""
from sport_activities_features import DataAnalysis

# Instantiate DataAnalysis object instance.
data_analysis = DataAnalysis()

# try to find the best possible classification pipeline for
# the given data in the form of CSV file (see example in the
# read_all_files.csv).

# see NiaAML's documentation for further details on possible
# input parameters' values (fitness_name, population_size,
# number_of_evaluations, optimization_algorithm, classifiers,
# feature_selection_algorithms, feature_transform_algorithms, imputer).
pipeline = data_analysis.analyze_data(
    '<path_to_CSV>',
    'Accuracy',
    20,
    400,
    'DifferentialEvolution',
    ['AdaBoost', 'Bagging', 'MultiLayerPerceptron'],
    ['SelectKBest', 'SelectPercentile', 'ParticleSwarmOptimization'],
    ['Normalizer', 'StandardScaler'],
)

# see NiaAML's documentation for further details on export options
# export the optimized pipeline for later use
pipeline.export('<export path>')
# export the optimized pipeline in a user-friendly text form
pipeline.export_text('<export path>')

# load the exported binary pipeline
imported_pipeline = data_analysis.load_pipeline(
    '<path to binary pipeline file>',
)

# in order to run classification, the method run should be
# called using the Pipeline instance:
# where x is a Pandas DataFrame where each line is an individual
# to be classified and each row represents the individual's feature
