from srcs.get_range import get_distance
from srcs.get_greatercircle import greatcircle
# Creates geojson feature with geometry Linestring
# Input type expected same as a single candidate dict from get_information()

def create_linestring(origin, destination, id):
	new = dict()
	new['type'] = "Feature"
	new['id'] = id
	geometry = dict()
	geometry['type'] = "LineString"
	org_p = [origin['geometry']['location']['lng'], origin['geometry']['location']['lat']]
	dest_p = [destination['geometry']['location']['lng'], destination['geometry']['location']['lat']]
	multi, geometry['coordinates'] = greatcircle(org_p, dest_p, 100)
	if multi:
		geometry['type'] = "MultiLineString"
	new['geometry'] = geometry
	props = dict()
	props['origin'] = origin['name']
	props['destination'] = destination['name']
	props['distance'] = get_distance(org_p[1], org_p[0], dest_p[1], dest_p[0])
	props['formatted_address'] = destination['formatted_address']
	if "website" in destination.keys():
		props['website'] = destination['website']
	else:
		props['website'] = None
	new['properties'] = props
	return new
