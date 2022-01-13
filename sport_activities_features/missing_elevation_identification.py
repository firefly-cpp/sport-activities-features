import json
import requests

class ElevationIdentification():
    """
    Class for retrieving elevation data using Open Elevation Api.
    """
    def __init__(self, open_elevation_api="https://api.open-elevation.com/api/v1/lookup", positions=[]):
        """
        Args:
            open_elevation_api: Address of the Open Elevation Api, default https://api.open-elevation.com/api/v1/lookup
            positions: [(lat1, lon1), (lat2, lon2) ...] - List of touples of latitudes and longitudes
        """
        self.open_elevation_api = open_elevation_api
        self.positions = positions
    def __map_payload(self, position):
        return {
            "latitude": float(position[0]),
            "longitude": float(position[1]),
        }

    def __divide_chunks(self, elements, n):
        """
        Helper function so that HTTP requests aren't too big
        :param elements: list of elements
        :param n: number of elements in a chunk
        :return: list of chunks
        """
        for i in range(0, len(elements), n):
            yield elements[i:i + n]

    def fetch_elevation_data(self, payload_formatting=True):
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