import argparse
from pathlib import Path
import trimesh
import numpy as np
from PIL import Image
import sys
import json
from math import *
import math
import requests
import geopandas as gpd

import matplotlib.pyplot as plt


argv = sys.argv
argv = [element if "--" not in element else "" for element in argv]
argv = [x for x in argv if x != ""]

#all arguments
method = argv[1]
GPSauto = argv[2]
pointCustom = (float(argv[3]), float(argv[4]))
dist = int(argv[5])
path = argv[8]
finalFp = argv[7]

#what method of localisation
if method == "auto":
    # Opening JSON file
    with open(GPSauto, 'r') as inputfile:
    
        # Reading from json file
        json_object = json.load(inputfile)
    
    latitude = json_object["latitude"]
    longitude = json_object["longitude"]

    point=(latitude, longitude)
else:
    point = pointCustom

print(point)

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)


lon_deg = point[1]
lat_rad = point[0]

print(lon_deg, lat_rad)

zoom = 15

xtile, ytile = deg2num(lat_deg=lat_rad, lon_deg=lon_deg, zoom=zoom)

print(xtile, ytile)


url = "https://data.osmbuildings.org/0.2/anonymous/tile/{0}/{1}/{2}.json".format(zoom, xtile, ytile) 
agentheader = {'User-Agent': 'PostmanRuntime/7.28.4'}

response = requests.get(url,headers = agentheader)

data = json.loads(response.text)


with open(finalFp, 'w') as f:
  json.dump(data, f)
  

gdf = gpd.read_file(finalFp)

