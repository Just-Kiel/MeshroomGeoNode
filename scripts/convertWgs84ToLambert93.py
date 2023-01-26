from pyproj import Transformer
import json

#TODO json to dict
def convertGPSDataToLambert93(GPSData):
    # Opening JSON file
    with open(GPSData, 'r') as inputfile:
        # Reading from json file
        json_object = json.load(inputfile)
    
    latitude = json_object["latitude"]
    longitude = json_object["longitude"]

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x,y =transformer.transform(latitude, longitude)

    # Data to be written
    output = {
        "latitude": x,
        "longitude": y
    }

    # Serializing json
    json_object = json.dumps(output, indent=4)
    return json_object