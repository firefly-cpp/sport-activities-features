import json
from geopy import distance
import overpy
import requests
import math


class OverpyNodesReader(object):
    r"""Working with Overpass (Overpy) nodes"""

    def __init__(self, open_elevation_api):
        self.open_elevation_api = open_elevation_api

    def __map_payload(self, node):
        return {
            "latitude": float(node.lat),
            "longitude": float(node.lon),
        }

    def read_nodes(self, nodes):
        r"""Parse one nodes list.

        Returns:
            dictionary:
        """
        activity_type = "Overpy nodes"

        positions = []
        altitudes = []
        distances = []

        nodes = list(map(self.__map_payload, nodes))

        payload = {"locations": nodes}
        json_data = requests.post(url=self.open_elevation_api, json=payload).content
        data = json.loads(json_data)
        for node in data["results"]:
            altitudes.append(node["elevation"])

        node: overpy.node
        prevNode = nodes[0]

        for i in range(len(nodes)):
            node = nodes[i]
            positions.append((node["latitude"], node["longitude"]))
            if i != 0:
                flat_distance = distance.distance(
                    (node["latitude"], node["longitude"]),
                    (prevNode["latitude"], prevNode["longitude"]),
                ).meters
                euclidean_distance = math.sqrt(
                    flat_distance ** 2 + abs(altitudes[i] - altitudes[i - 1]) ** 2
                )
                distances.append(euclidean_distance)
            else:
                distances.append(0)
            prevNode = node
        try:
            total_distance = sum(distances)
        except BaseException:
            total_distance = None

        interpreted_way = {
            "activity_type": activity_type,
            "positions": positions,
            "altitudes": altitudes,
            "distances": distances,
            "total_distance": total_distance,
        }

        return interpreted_way
