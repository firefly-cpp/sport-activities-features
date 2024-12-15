from sport_activities_features import GPXFile

# read GPX file
gpx_file = GPXFile()
gpx_exercise = gpx_file.read_one_file('path_to_the_file')
data = gpx_file.extract_activity_data(gpx_exercise)
