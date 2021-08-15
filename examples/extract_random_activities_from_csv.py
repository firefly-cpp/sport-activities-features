import sys

sys.path.append("../")

from sport_activities_features.data_extraction_from_csv import DataExtractionFromCSV

data_extraction_from_csv = DataExtractionFromCSV()
# Extract data from CSV file to dataframe
activities = data_extraction_from_csv.from_file("<path_to_CSV>")
# With the obtained data we can review e.g. how many different types of activities we have
print(activities["activity_type"].value_counts())

# Selection of a certain number of random activities
random_activities = data_extraction_from_csv.select_random_activities(3)
print(random_activities)


# Extract data to list of dataframes from all CSV files in the folder
list_dfs = data_extraction_from_csv.from_all_files("path_to_the_folder")
# From the obtained dataframes we can print e.g. the first 5 activities
# If a file parsing error occurs (if it has the wrong structure), a message is displayed.
for df in list_dfs:
    print(df.head())
    print("_______")
