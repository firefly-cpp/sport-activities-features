import json
import requests

class ElevationIdentification():
    """
    Class for retrieving elevation data using Open Elevation Api.
    """
    def __init__(self, open_elevation_api="https://api.open-elevation.com/api/v1/lookup", positions=[]):
        """
        Initialisation method for ElevationIdentification.
        Args:
            open_elevation_api: Address of the Open Elevation Api, default https://api.open-elevation.com/api/v1/lookup
            positions: [(lat1, lon1), (lat2, lon2) ...] - List of touples of latitudes and longitudes
        """
        self.open_elevation_api = open_elevation_api
        self.positions = positions
    def __map_payload(self, position:(float, float)):
        """
        Method that converts touple into JSON like object for equerying the Open Elevation API.
        Args:
            position: touple of latitude and longitude

        Returns: JSON like object {
            "latitude": float(position[0]),
            "longitude": float(position[1]),
        }
        """
        return {
            "latitude": float(position[0]),
            "longitude": float(position[1]),
        }

    def __divide_chunks(self, elements, n:int):
        """
        Helper function so that HTTP requests aren't too big. It breaks up a list of elements into smaller lists of
        elements of size n.
        Args:
            elements: list of elements to be broken into chunks
            n: number of elements in a chunk
        Returns: list of chunks (lists)
        """
        for i in range(0, len(elements), n):
            yield elements[i:i + n]

    def fetch_elevation_data(self, payload_formatting:bool=True):
        """
        Method for making requests to the Open Elevation API to retrieve elevation data
        Args:
            payload_formatting: True -> break into chunks, False -> don't break self.positions into chunks
        Returns: elevations : [int] list of elevations for the given positions
        """
        open_elevation_nodes = []
        if payload_formatting:
            open_elevation_nodes = list(map(self.__map_payload, self.positions))
        else:
            open_elevation_nodes=self.positions
        l=len(open_elevation_nodes)/150
        chunks = self.__divide_chunks(open_elevation_nodes, 150)
        elevations = []
        i=0
        for chunk in chunks:
            payload = {"locations": chunk}
            json_data = requests.post(url=self.open_elevation_api, json=payload).content
            data = json.loads(json_data)['results']
            for result in data:
                elevations.append(result['elevation'])
            i+=1
        return elevations