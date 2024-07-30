import http.client
import json
import urllib.parse
from enum import Enum

class ElevationApiType(Enum):
    OPEN_ELEVATION_API = 1
    OPEN_TOPO_DATA_API = 2

class ElevationIdentification():

    """Class for retrieving elevation data using Elevation Api, Open-Elevation API and OpenTopoData API supported.\n
    Args:
        open_elevation_api (str):
            address of the Api,
            default https://api.open-elevation.com/api/v1/lookup
        positions (list[(lat1, lon1), (lat2, lon2) ...]):
            list of tuples of latitudes and longitudes.
    """

    def __init__(
        self,
        open_elevation_api:
            str = 'https://api.open-elevation.com/api/v1/lookup',
        positions: list = [],
        open_topo_data_api:
            str = 'https://api.opentopodata.org/v1/srtm90m',
        elevation_api_type: ElevationApiType = ElevationApiType.OPEN_ELEVATION_API,
    ) -> None:
        """Initialisation method for ElevationIdentification class.\n
        Args:
        open_elevation_api (str):
            address of the Elevation Api,
            default https://api.open-elevation.com/api/v1/lookup
        positions (list[(lat1, lon1), (lat2, lon2) ...]):
            list of tuples of latitudes and longitudes.
        open_topo_data_api (str):
            address of the Open Topo Data API,
        elevation_api_type (ElevationApiType):
            type of the elevation API to be used, default OPEN_ELEVATION_API.
        """
        self.open_elevation_api = open_elevation_api
        self.positions = positions
        self.elevation_api_type = elevation_api_type
        self.open_topo_data_api = open_topo_data_api

    def __map_payload_open_elevation_api(self, position: tuple) -> dict:
        """Method that converts tuple into JSON like object
        for equerying the Open Elevation API.\n
        Args:
            position (tuple):
                tuple of latitude and longitude
        Returns:
            JSON like object {
                'latitude': float(position[0]),
                'longitude': float(position[1]),
            }.
        """
        return {
            'latitude': float(position[0]),
            'longitude': float(position[1]),
        }

    def __divide_chunks(self, elements: list, n: int) -> list:
        """Helper function so that HTTP requests aren't too big.
        It breaks up a list of elements into smaller lists of
        elements of size n.\n
        Args:
            elements (list):
                list of elements to be broken into chunks
            n (int):
                number of elements in a chunk
        Returns:
            list: list of chunks (lists).
        """
        for i in range(0, len(elements), n):
            yield elements[i:i + n]

    def fetch_elevation_data(self, payload_formatting: bool = True) -> list:
        """Method for making requests to the Elevation API
               to retrieve elevation data.\n
               Args:
                   payload_formatting (bool):
                       True -> break into chunks,
                       False -> don't break self.positions into chunks
               Returns:
                   list[int]: list of elevations for the given positions.
               """
        if self.elevation_api_type == ElevationApiType.OPEN_ELEVATION_API:
            return self.fetch_open_elevation_data(payload_formatting)
        elif self.elevation_api_type == ElevationApiType.OPEN_TOPO_DATA_API:
            return self.fetch_open_topo_data(payload_formatting)
        else:
            raise ValueError("Invalid Elevation API Type")
    def fetch_open_topo_data(self, payload_formatting: bool = True) -> list:
        """Method for making requests to the Open Topo Data API
        to retrieve elevation data.\n
        Args:
            payload_formatting (bool):
                True -> break into chunks,
                False -> don't break self.positions into chunks
        Returns:
            list[int]: list of elevations for the given positions.
        """
        open_topo_nodes = []
        chunks = self.__divide_chunks(self.positions, 100) # into 100 because of the default limit of the API
        elevations = []

        for chunk in chunks:
            coordinate_string = '|'.join([','.join(map(str, coord)) for coord in chunk])
            payload = {"locations": coordinate_string,
                       "interpolation": "cubic"}
            json_payload = json.dumps(payload)  # Convert payload to JSON string

            headers = {"Content-Type": "application/json"}

            # Split the URL into host and path
            url_parts = urllib.parse.urlparse(self.open_topo_data_api)
            host = url_parts.netloc
            path = url_parts.path

            # Establish connection
            if self.open_elevation_api.startswith("http://"):
                connection = http.client.HTTPConnection(host)
            else:
                connection = http.client.HTTPSConnection(host)

            # Make the POST request
            connection.request("POST", path, body=json_payload, headers=headers)

            # Get the response
            response = connection.getresponse()
            response_data = response.read().decode('utf-8')

            # Close the connection
            connection.close()

            # Parse the response data
            data = json.loads(response_data)['results']
            for result in data:
                elevations.append(result['elevation'])
        return elevations


    def fetch_open_elevation_data(self, payload_formatting: bool = True) -> list:
        """Method for making requests to the Open Elevation API
        to retrieve elevation data.\n
        Args:
            payload_formatting (bool):
                True -> break into chunks,
                False -> don't break self.positions into chunks
        Returns:
            list[int]: list of elevations for the given positions.
        """
        open_elevation_nodes = []
        if payload_formatting:
            open_elevation_nodes = list(
                map(self.__map_payload_open_elevation_api, self.positions),
            )
        else:
            open_elevation_nodes = self.positions
        chunks = self.__divide_chunks(open_elevation_nodes, 150)
        elevations = []
        i = 0
        for chunk in chunks:
            payload = {'locations': chunk}
            json_payload = json.dumps(payload)  # Convert payload to JSON string
            headers = {"Content-Type": "application/json"}

            # Split the URL into host and path
            url_parts = urllib.parse.urlparse(self.open_elevation_api)
            host = url_parts.netloc
            path = url_parts.path

            # Establish connection
            if self.open_elevation_api.startswith("http://"):
                connection = http.client.HTTPConnection(host)
            else:
                connection = http.client.HTTPSConnection(host)

            # Make the POST request
            connection.request("POST", path, body=json_payload, headers=headers)

            # Get the response
            response = connection.getresponse()
            response_data = response.read().decode('utf-8')

            # Close the connection
            connection.close()

            # Parse the response data
            data = json.loads(response_data)['results']
            for result in data:
                elevations.append(result['elevation'])
            i += 1
        return elevations