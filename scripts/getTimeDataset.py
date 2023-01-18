import argparse
import json
from timezonefinder import TimezoneFinder
from datetime import datetime
from dateutil import tz

ap = argparse.ArgumentParser()
ap.add_argument("inputFile", help="input SFM data", type=str)
ap.add_argument("GPSFile", help="GPSFile", type=str)
ap.add_argument("output", help="output", type=str)
args = ap.parse_args()

# Opening JSON file
with open(args.inputFile, 'r') as inputfile:
    # Reading from json file
    json_object = json.load(inputfile)

date = json_object["views"][0]["metadata"]["Exif:DateTimeOriginal"]

if "Exif:OffsetTimeOriginal" in json_object["views"][0]["metadata"]:
    offsetTime = json_object["views"][0]["metadata"]["Exif:OffsetTimeOriginal"]
    offsetTime = offsetTime.replace(":", ".")
    offsetTime = int(float(offsetTime))
else:
    # Opening JSON file
    with open(args.GPSFile, 'r') as GPSfile:
        # Reading from json file
        json_gps = json.load(GPSfile)
    
    tf = TimezoneFinder()

    timezone = tf.timezone_at(lng=json_gps["longitude"], lat=json_gps["latitude"])

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(timezone)
    start_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")

    start_date = start_date.replace(tzinfo = from_zone)
    local = start_date.astimezone(to_zone)

    local = [x for x in str(local.utcoffset()).split(':')]

    offsetTime = int(local[0])
    



date = date.replace(" ", ":")

date = [x for x in date.split(":")]

# Data to be written
output = {
    "datetime": date,
    "offsetTime": offsetTime
}

# Serializing json
json_object = json.dumps(output, indent=4)

# Writing to sample.json
with open(args.output, "w") as outfile:
    outfile.write(json_object)