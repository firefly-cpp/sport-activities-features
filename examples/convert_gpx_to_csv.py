"""Convert GPX file to CSV file."""
import pandas as pd

from sport_activities_features.gpx_manipulation import GPXFile

# Class for reading GPX files
gpx_file = GPXFile()

# Path to input GPX file
input_file = 'path_to_original_file'
# Path to newly created output CSV file
output_file = 'path_to_output_file'

# Read GPX file
data = gpx_file.read_one_file(
    input_file,
)  # Represents data as dictionary of lists

# Convert dictionary of lists to pandas DataFrame
gpx_to_csv_df = pd.DataFrame.from_dict(data)

# Set index name
gpx_to_csv_df.index.name = 'row_id'

# Save DataFrame to CSV file with semicolon as separator
gpx_to_csv_df.to_csv(output_file, sep=';')
