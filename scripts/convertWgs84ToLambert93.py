from pyproj import Transformer
import argparse
import json

# get arguments
ap = argparse.ArgumentParser()
ap.add_argument("method", help="method of gps", type=str)
ap.add_argument("GPSFile", help="GPSFile", type=str)
ap.add_argument("latitudeCustom", help="latitudeCustom", type=float)
ap.add_argument("longitudeCustom", help="longitudeCustom", type=float)
ap.add_argument("outputFile", help="outputFile", type=str)
args = ap.parse_args()


if args.method == "auto":
    # Opening JSON file
    with open(args.GPSFile, 'r') as inputfile:
    
        # Reading from json file
        json_object = json.load(inputfile)
    
    latitude = json_object["latitude"]
    longitude = json_object["longitude"]
else:
    latitude = args.latitudeCustom
    longitude = args.longitudeCustom

transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
x,y =transformer.transform(latitude, longitude)

x=(x/1000) #meters to km
y=(y/1000)

# for x
x = int(x) if int(x)%2==0 else int(x)+1

# for y
y = int(y) if int(y)%2!=0 else int(y)+1


# Data to be written
output = {
    "latitude": x,
    "longitude": y
}

# Serializing json
json_object = json.dumps(output, indent=4)

# Writing to sample.json
with open(args.outputFile, "w") as outfile:
    outfile.write(json_object)