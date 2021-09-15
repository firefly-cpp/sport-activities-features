import overpy
from sport_activities_features.overpy_node_manipulation import OverpyNodesReader

# External service Overpass API (https://wiki.openstreetmap.org/wiki/Overpass_API) (can be self hosted)
overpass_api = "https://lz4.overpass-api.de/api/interpreter"

# External service Open Elevation API (https://api.open-elevation.com/api/v1/lookup) (can be self hosted)
open_elevation_api = "https://api.open-elevation.com/api/v1/lookup"

# OSM Way (https://wiki.openstreetmap.org/wiki/Way)
open_street_map_way = 164477980

overpass_api = overpy.Overpass(url=overpass_api)

# Get an example Overpass way
q = f"""(way({open_street_map_way});<;);out geom;"""
query = overpass_api.query(q)

# Get nodes of an Overpass way
nodes = query.ways[0].get_nodes(resolve_missing=True)

# Extract basic data from nodes (you can later on use Hill Identification and Hill Data Extraction on them)
overpy_reader = OverpyNodesReader(open_elevation_api=open_elevation_api)
# Returns {
#         'positions': positions, 'altitudes': altitudes, 'distances': distances, 'total_distance': total_distance
#         }
data = overpy_reader.read_nodes(nodes)
