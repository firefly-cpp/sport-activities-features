import csv


class DataExtraction(object):
    def __init__(self, activities):
        self.activities = activities

    # Writing each activity data as CSV
    def extract_data(self, path):
        with open(
            path + ".csv" if not path.endswith(".csv") else path, mode="w", newline=""
        ) as csv_file:
            fieldnames = [
                "id",
                "duration",
                "distance",
                "calories",
                "number_of_hills",
                "distance_between_hills",
                "number_of_intervals",
                "average_interval_duration",
                "longest_interval",
                "activity_type",
            ]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            # Output of each activity
            for activity in self.activities:
                csv_writer.writerow(
                    {
                        "id": activity["ID"],
                        "duration": activity["duration"],
                        "distance": activity["distance"],
                        "calories": activity["calories"],
                        "number_of_hills": activity["number_of_hills"],
                        "distance_between_hills": activity["distance_between_hills"],
                        "number_of_intervals": activity["number_of_intervals"],
                        "average_interval_duration": activity["avg_duration_interval"],
                        "longest_interval": activity["max_duration_interval"],
                        "activity_type": activity["activity_type"],
                    }
                )
