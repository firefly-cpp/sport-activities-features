"""Convert TCX file to CSV file."""
import pandas as pd
from sport_activities_features.tcx_manipulation import TCXFile

# Class for reading TCX files
tcx_file = TCXFile()

# Path to input TCX file
input_file = 'path_to_original_file'
# Path to newly created output CSV file
output_file = 'path_to_output_file'

# Read TCX file
data = tcx_file.read_one_file(
    input_file,
)  # Represents data as dictionary of lists

# Convert dictionary of lists to pandas DataFrame
tcx_to_csv_df = pd.DataFrame.from_dict(data)

# Set index name
tcx_to_csv_df.index.name = 'row_id'

# Save DataFrame to CSV file with semicolon as separator
tcx_to_csv_df.to_csv(output_file, sep=";")
