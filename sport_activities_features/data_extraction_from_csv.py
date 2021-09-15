import os
import pandas as pd


class DataExtractionFromCSV(object):
    def __init__(self, activities=None):
        self.activities = activities

    # Extract data from CSV file to dataframe
    def from_file(self, path):
        with open(
            path + ".csv"
            if not (path.endswith(".csv") or path.endswith(".txt"))
            else path
        ) as csv_file:
            try:
                self.activities = pd.read_csv(
                    csv_file, index_col=0, sep=",", decimal="."
                )
                return self.activities
            except:
                print("Incorrect structure of file " + str(csv_file.name))
                return pd.DataFrame()

    # Extract data to list of dataframes from all CSV files in the folder
    def from_all_files(self, path):
        if not path.endswith("/"):
            path = path + "/"

        for root, dirs, files in os.walk(path):
            dataframes = []
            for file in files:
                if file.endswith(".csv") or file.endswith(".txt"):
                    df = self.from_file(path + file)
                    if not df.empty:
                        dataframes.append(df)
            return dataframes

    def select_random_activities(self, number) -> None:
        if self.activities is None:
            print("No activities")
        elif len(self.activities) >= number:
            return self.activities.sample(number, replace=False)
        else:
            print(
                "The number of activities is lower than the size of the desired sample"
            )
            return self.activities
