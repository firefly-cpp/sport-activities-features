import json
import requests


class ElevationIdentification():
    """
    Class for retrieving elevation data using Open Elevation Api.\n
    Args:
        open_elevation_api (str):
            address of the Open Elevation Api,
            default https://api.open-elevation.com/api/v1/lookup
        positions (list[(lat1, lon1), (lat2, lon2) ...]):
            list of tuples of latitudes and longitudes
    """
    def __init__(
        self,
        open_elevation_api:
            str = 'https://api.open-elevation.com/api/v1/lookup',
        positions: list = []
    ) -> None:
        """
        Initialisation method for ElevationIdentification class.\n
    Args:
        open_elevation_api (str):
            address of the Open Elevation Api,
            default https://api.open-elevation.com/api/v1/lookup
        positions (list[(lat1, lon1), (lat2, lon2) ...]):
            list of tuples of latitudes and longitudes
        """
        self.open_elevation_api = open_elevation_api
        self.positions = positions

    def __map_payload(self, position: tuple) -> dict:
        """
        Method that converts tuple into JSON like object
        for equerying the Open Elevation API.\n
        Args:
            position (tuple):
                tuple of latitude and longitude
        Returns:
            JSON like object {
                'latitude': float(position[0]),
                'longitude': float(position[1]),
            }
        """
        return {
            'latitude': float(position[0]),
            'longitude': float(position[1]),
        }

    def __divide_chunks(self, elements: list, n: int) -> list:
        """
        Helper function so that HTTP requests aren't too big.
        It breaks up a list of elements into smaller lists of
        elements of size n.\n
        Args:
            elements (list):
                list of elements to be broken into chunks
            n (int):
                number of elements in a chunk
        Returns:
            list: list of chunks (lists)
        """
        for i in range(0, len(elements), n):
            yield elements[i:i + n]

    def fetch_elevation_data(self, payload_formatting: bool = True) -> list:
        """
        Method for making requests to the Open Elevation API
        to retrieve elevation data.\n
        Args:
            payload_formatting (bool):
                True -> break into chunks,
                False -> don't break self.positions into chunks
        Returns:
            list[int]: list of elevations for the given positions
        """
        open_elevation_nodes = []
        if payload_formatting:
            open_elevation_nodes = list(
                map(self.__map_payload, self.positions)
            )
        else:
            open_elevation_nodes = self.positions
        chunks = self.__divide_chunks(open_elevation_nodes, 150)
        elevations = []
        i = 0
        for chunk in chunks:
            payload = {"locations": chunk}
            json_data = requests.post(
                url=self.open_elevation_api,
                json=payload
            ).content
            data = json.loads(json_data)['results']
            for result in data:
                elevations.append(result['elevation'])
            i += 1
        return elevations
