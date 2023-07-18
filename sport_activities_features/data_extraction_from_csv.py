import os

import pandas as pd


class DataExtractionFromCSV:

    """Class for extracting data from CSV files.\n
    Args:
        activities (list):
            list of activities.
    """

    def __init__(self, activities: list = None) -> None:
        """Initialisation method for DataExtractionFromCSV class.\n
        Args:
            activities (list):
                list of activities.
        """
        self.activities = activities

    def from_file(self, path: str) -> list:
        """Method for extracting data from CSV file to dataframe.\n
        Args:
            path (str): absolute path to the CSV file
        Returns:
            list: list of activities.
        """
        with open(
            path + '.csv'
            if not (path.endswith(('.csv', '.txt')))
            else path,
        ) as csv_file:
            try:
                self.activities = pd.read_csv(
                    csv_file, index_col=0, sep=',', decimal='.',
                )
                return self.activities
            except Exception:
                print('Incorrect structure of file ' + str(csv_file.name))
                return pd.DataFrame()

    def from_all_files(self, path: str) -> list:
        """Method for extracting data to list of dataframes
        from all CSV files in the folder.\n
        Args:
            path (str):
                absolute path to the folder with CSV files
        Returns:
            list: list of activities.
        """
        if not path.endswith('/'):
            path = path + '/'

        for _root, _dirs, files in os.walk(path):
            dataframes = []
            for file in files:
                if file.endswith(('.csv', '.txt')):
                    df = self.from_file(path + file)
                    if not df.empty:
                        dataframes.append(df)
            return dataframes
        return None

    def select_random_activities(self, number: int) -> list:
        """Method for selecting random activities.\n
        Args:
            number (int):
                desired number of random activities
        Returns:
            list: list of random activities.
        """
        if self.activities is None:
            print('No activities')
            return None
        elif len(self.activities) >= number:
            return self.activities.sample(number, replace=False)
        else:
            print(
                'The number of activities is lower ',
                'than the size of the desired sample',
            )
            return self.activities
