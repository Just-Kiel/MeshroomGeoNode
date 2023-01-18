# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Hourly

import argparse
from pathlib import Path
import json

# get arguments
ap = argparse.ArgumentParser()
ap.add_argument("method", help="method of gps", type=str)
ap.add_argument("GPSFile", help="GPSFile", type=str)
ap.add_argument("latitudeCustom", help="latitudeCustom", type=float)
ap.add_argument("longitudeCustom", help="longitudeCustom", type=float)
ap.add_argument("timeFile", help="timeFile", type=str)
ap.add_argument("outputFile", help="outputFile", type=str)
args = ap.parse_args()

# get coordinates
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

# get date
with open(args.timeFile, 'r') as inputfile:
    
    # Reading from json file
    json_object = json.load(inputfile)

time = json_object["datetime"]

#add jet lag to time
offsetTime = json_object["offsetTime"]
time.append(offsetTime)

datefile = tuple(int(element) for element in time)

year, month, day, hour, minute, second, timezone = datefile

# Set time period
ymd = datetime(year, month, day)

# Create Point from coordinates
location = Point(latitude, longitude)

# Get Weather Hourly data from the coordinates
data = Hourly(location, ymd, ymd)
data = data.fetch()

# Data to be written
output = {
    "temperature": data['temp'][0],
    "humidity": data['rhum'][0],
    "wind direction": data['wdir'][0],
    "wind speed": data['wspd'][0],
    "weather condition": data['coco'][0]
}

# Serializing json
json_object = json.dumps(output, indent=4)

# Writing to sample.json
with open(args.outputFile, "w") as outfile:
    outfile.write(json_object)