import json
import requests

#Google Places API token
token = "<your_token>"

def	get_place_details(input):
	inputtype = "textquery"
	candidates = list()
	# Fetch place_id from Google
	ret = requests.get(f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={input}&inputtype={inputtype}&key={token}")

	if  ret.status_code == 200:
		tmp = ret.json()
		for candidate in tmp['candidates']:
			place_id = candidate['place_id']
			# Fetch details about the place
			# data return specification
			fields = "formatted_address,name,geometry,website,place_id"
			details = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={token}&fields={fields}")
			if details.status_code == 200:
				tmp = details.json()
				candidates.append(tmp['result'])
	if len(candidates) == 0:
		return None
	else:
		return candidates

if __name__ == "__main__":
	instr = input("Search Querry:\n")
	ret = get_place_details(instr  + " capital city")
	print("Results:")
	print(json.dumps(ret, indent=4))
