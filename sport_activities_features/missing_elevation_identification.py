import json
import requests

class ElevationIdentification():
    def __init__(self, open_elevation_api="http://zabojnik.informatika.uni-mb.si:8086/api/v1/lookup", positions=[]):
        self.open_elevation_api = open_elevation_api
        self.positions = positions
    def map_payload(self, position):
        return {
            "latitude": float(position[0]),
            "longitude": float(position[1]),
        }

    def divide_chunks(self, elements, n):
        """
        :param elements: list of elements
        :param n: number of elements in a chunk
        :return: list of chunks
        """
        for i in range(0, len(elements), n):
            yield elements[i:i + n]

    def fetch_elevation_data(self):
        open_elevation_nodes = list(map(self.map_payload, self.positions))
        l=len(open_elevation_nodes)/150
        chunks = self.divide_chunks(open_elevation_nodes, 150)
        elevations = []
        i=0
        for chunk in chunks:
            payload = {"locations": chunk}
            json_data = requests.post(url="http://zabojnik.informatika.uni-mb.si:8086/api/v1/lookup", json=payload).content
            data = json.loads(json_data)['results']
            for result in data:
                elevations.append(result['elevation'])
            i+=1
        return elevations