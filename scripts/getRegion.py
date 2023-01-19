# import module
from geopy.geocoders import Nominatim
import json
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("GPSFile", help="GPSFile", type=str)
ap.add_argument("output", help="output", type=str)
args = ap.parse_args()

# Opening JSON file
with open(args.GPSFile, 'r') as GPSfile:
    # Reading from json file
    json_gps = json.load(GPSfile)


# initialize Nominatim API
geolocator = Nominatim(user_agent="getRegion")
# Latitude & Longitude input
Latitude = json_gps["latitude"]
Longitude = json_gps["longitude"]
 
location = geolocator.reverse(str(Latitude)+","+str(Longitude))

address = location.raw['address']

# Data to be written
output = {
    "region": address["county"],
    "postcode": address["postcode"]
}

# Serializing json
json_object = json.dumps(output, indent=4)

# Writing to sample.json
with open(args.output, "w") as outfile:
    outfile.write(json_object)