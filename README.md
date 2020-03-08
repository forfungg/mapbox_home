# MapBox Home Assignment 2020

The result version 1.0 can be found [here](https://jiricodes.com/mapbox)

## Usage

### Interactive map

Open index.html in your browser. Or visit [https://jiricodes.com/mapbox](https://jiricodes.com/mapbox).

### GeoJSON generator

Requirements:
```
#Python3
python3
#Requests Module
pip3 install requests
#Google Places API token
```

Open srcs/get_information.py and copy your token to line 5:
```
#Google Places API token
token = "<your_token>"
```

Run:
```
python3 create_geojson.py
```

Upon the prompt, insert name of your desired origin capital city (e.g. Helsinki). After initial information is fetched and confirmed, insert path/filename to your list of desired 'destination cities'.

Output result is saved to my_geolist.geojson.

## Features

- rendered by Mapbox GL JS
- lines connecting every capital to Helsinki
- styled map to improve data visualization
- lines rendered on the map using [great circle distances](https://en.wikipedia.org/wiki/Great-circle_distance)
- lines colored according to the distance
- line color changed to white when hovering over
- a popup label above a line on click, displays "connection" name, distance and link to destination's webpage if available
- fullscreen mode

## Approach and Reasoning

### Dataset

Finding and obtaining correct set of data turned out to be a bit more complicated than expected, since the definition of capital city is not that exact. Depending whether the cities of interest are solely [national capitals](https://www.thoughtco.com/capitals-of-every-independent-country-1434452) or they include as well [capitals of territories, dependencies or even disputed regions.](https://en.wikipedia.org/wiki/List_of_national_capitals)

So I've decided to create a python script that accepts a 'origin city' input and a file containing list of 'destination' cities (one per line). It collects data from Google Places API for each city and creates features that are then written into a geojson file.

This way any definition of capital city can be satisfied by users themselves or they might create lines between any desired cities (would require small tweak in search query for Google's API).

Specific geo-oriented API would be preferable over Google Places API, however due to time constraints and availablity it served as reliable enough source for this assigment.

For the sake of this assignment I've chosen to plot only lines connecting to capitals of indenpendent countries.

### Styling in Studio

After generating desired geojson, I've used [Tippecanoe](https://github.com/mapbox/tippecanoe) to create vector tiles.

```
tippecanoe -o hki-cpt.mbtiles -zg -l hki-lines -n "Helsinki to other capitals connections" -ai my_geolist.geojson
```

Then I've used Mapbox Studio to style my map and the tileset, removing some unnecessary layers and improving visibility.

### MapBox GL JS

Finally I've used MapBox GL JS to plot the map and create interaction in a web browser. This was quite a bit challenging since I've not worked with JavaScript before. Nonetheless the exploration and difficulty was very enjoyable in the end.
I've heavily benefited from MapBox's documentation, tutorials and deduction based on my knowledge of coding principles from C and python.

## Code Wiki

### create_geojson.py
Python script that creates GeoJSON file containing feature collection of LineStrings and MultiLineStrings that connect with given origin capital city to all cities in given file. The should contain only one capital city per line, otherwise results may vary from what's desired.

Input:\\
- first prompt - origin capital city
- second prompt - file that contains list of destination capital cities

Output:\\
my_geolist.geojson

### create_feature.py

**create_linestring()**

Creates GeoJSON compatible feature.

Parametres:\\
- origin - dict object, expected in the same format as output of get_place_details(). Used as origin for generated LineString
- destination - dict object, expected in the same format as output of get_place_details(). Used as destination for generated LineString
- id - numerical value to be assigned as feature's id (recommended to be unique per feature)

Output:\\
Dict object suitable to be inserted as Feature of LineString/MultiLineString type into feature collection of a GeoJSON.

Output Example:
```
{
            "type": "Feature",
            "id": id,
            "geometry": {
                "type": "LineString",
                "coordinates": [great_circle_coordinates]
            },
            "properties": {
                "origin": "origin_name",
                "destination": "destination_name",
                "distance": great_circle_distance_in_metres,
                "formatted_address": "destination_address",
                "website": "destination_website"
            }
        }
```

### get_greatercircle.py

**get_greatercircle()**

Generates 'steps' amount of great circle coordinates between two given coordinates using translation between cartesian and eliptical coordinates.

Parametres:\\
- point1 - coordinates of starting point in format [longitude, latitude]
- point2 - coordinates of ending point in format [longitude, latitude]
- steps - amount of steps within the great circle (higher increases plotting precision, default = 100)

Output:\\
List of coordinates in format [point1, .. steps .. , point2]

**check_values()**

Checks coordinates of given great circle list whether there's is cross of longitude's extremes (180 to -180 or the other way). If such instance is detected the list is split with help of split_line() function and returned in format [[starting part] + [left approx transfer coord], [right approx transfer coord] + [ending part]].

Parametres:\\
- greater_circle - list of cordinates to be checked

Output:\\
- Boolean - True if the given list was split in two, False if the list was not changed
- greater_circle - list of great circle coordinates

Example:
Code
```
#point 1
p1 = [178.64209184022712, 2.598731224318669] 
#point 2
p2 = [-178.55927895810618, -8.60694107338936]
b, ret = check_values([p1, p2])
print(b)
print(ret)
```
Output
```
True
[[[178.64209184022712, 2.598731224318669], [179.9999999987759, -2.8675863404967807]], [[-179.99999999856297, -2.867586351189949], [-178.55927895810618, -8.60694107338936]]]
```

**split_line()**

Creates a coordinate on great circle close to longitude extreme depending on direction of the line with static error margin 0.00000000001. (this should be changed to be received as a parameter).

Parametres:\\
- p1 - starting point coordinates
- p2 - coordinates of a point on the oposite side of longitude extreme

Output:\\
Point in format [longitude, latitude] which is located on the p1 side of longitude extreme within error margin from the extreme itself.

### get_information.py

**get_place_details()**

Fetches data from Google Place API and Google Details API about given input and returns list of json formatted objects containing formatted_address, name, geometry, website, place_id fields. Returns 'None' if information retrieval fails.

Parametres:\\
- input - query string

Output:\\
List of dict objects containing formatted details about the search querry

Output example for 'Helsinki':
```
[
    {
        "formatted_address": "Laivurinkatu 37, 00150 Helsinki, Finland",
        "geometry": {
            "location": {
                "lat": 60.1593937,
                "lng": 24.9424996
            },
            "viewport": {
                "northeast": {
                    "lat": 60.16073943029151,
                    "lng": 24.9437608302915
                },
                "southwest": {
                    "lat": 60.1580414697085,
                    "lng": 24.9410628697085
                }
            }
        },
        "name": "Capital City Oy",
        "place_id": "ChIJgRc6t7cLkkYRoDyW4Z5EGDQ"
    }
]
```

### get_range()

**get_radius()**

Returns Earth's radius on given latitude

Parametres:\\
- lat - desired latitude

Output:\\
Numerical value in metres

**get_distance()**

Returns great circle distance between two points using average radius of Earth between the two of them. Originally designed to return users distance from a restaurant for [Wolt Internship Application](https://github.com/forfungg/woltapp2020).

Parametres:\\
- lat - point1 latitude
- lon - point1 longitude
- my_lat - users latitude
- my_long - users longitude

Output:\\
Numerical value in metres