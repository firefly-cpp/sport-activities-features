from geopy import distance
import overpy
import math
from sport_activities_features import ElevationIdentification


class OverpyNodesReader(object):
    r"""Working with Overpass (Overpy) nodes"""

    def __init__(self, open_elevation_api:str):
        """
        Args:
            open_elevation_api: Address of Open Elevation API, if a lot of altitudes are needed, self hosting is
            prefferable
        """
        self.open_elevation_api = open_elevation_api

    def __map_payload(self, node):
        return {
            "latitude": float(node.lat),
            "longitude": float(node.lon),
        }

    def read_nodes(self, nodes:overpy.Node):
        """
            Dictionary {

            "activity_type": "Overpy nodes",

            "positions": [(lat1, lon1), (lat2, lon2), ... (latN, lonN)], <- latitude, longitude touples

            "altitudes": altitudes, <- [alt1, alt2, ... altN] <- list of altitudes in meters

            "distances": distances, <- [d1, d2, ... dn] <- list of comulative distances between nodes,

            distances[dn] = distances[dn-1]+ ACTUAL DISTANCE BETWEEN N and N-1

            "total_distance": total_distance, <- total distance in meters }

        Args:
            nodes: List of overpy.Node objects

        Returns:
            { activity_type": str, "positions": [...], "altitudes": [...], "distances": [...], "total_distance": float}
        """
        activity_type = "Overpy nodes"

        positions = []
        altitudes = []
        distances = []

        nodes = list(map(self.__map_payload, nodes))
        elevation_identification = ElevationIdentification(open_elevation_api=self.open_elevation_api, positions=nodes)
        altitudes = elevation_identification.fetch_elevation_data(payload_formatting=False)

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
                distances.append(euclidean_distance+distances[-1])
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
