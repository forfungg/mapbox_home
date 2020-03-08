from srcs.get_information import get_place_details
from srcs.create_feature import create_linestring
import json
import os

def	check_if_duplicate(destinations, name):
	for d in destinations:
		if d['properties']['formatted_address'] == name:
			return True
	return False

# Select a City/Place to connect to your list of cities/places
while True:
	origin_name = input("Select origin city\nThis city will be treated as origin for all the connections:\n").capitalize()
	origin_data = get_place_details(origin_name)
	if not origin_data:
		print("\nGiven place hasn't been found in Google's API. Please try again.")
		continue
	else:
		origin = origin_data[0]
		print(f"\n{origin['formatted_address']} has been selected as origin.\nLongitude: {origin['geometry']['location']['lng']}\nLatitude: {origin['geometry']['location']['lat']}")
		break

while True:
	file_name = input("Select file containing destinations:\n")
	try:
		f = open(file_name, "r")
	except:
		print("Invalid file, try again.")
	else:
		break

cities = f.readlines()
geo = dict()
geo['type'] = "FeatureCollection"
features = list()
i = 0
print("Collecting Data")
for c in cities:
	new = get_place_details(c.rstrip().capitalize() + " capital city")
	if new:
		n = new[0]
		if not check_if_duplicate(features, n['formatted_address']) and n['formatted_address'] != origin['formatted_address']:
			feature = create_linestring(origin, n, i)
			features.append(feature)
			print(f"{i}: {n['formatted_address']}")
			i += 1
	else:
		print(f"Error adding {c} to the list of destinations. No information found.")

geo['features'] = features

with open("my_geolist.geojson", 'w') as f:
	json.dump(geo, f, indent=4)

print("Done!")