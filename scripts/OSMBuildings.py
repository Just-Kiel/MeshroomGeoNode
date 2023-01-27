import argparse
import trimesh
import numpy as np
import json
from math import *
import math
import requests
import geopandas as gpd
from shapely import Polygon

#TODO args better
ap = argparse.ArgumentParser()
ap.add_argument("--method", help="method of gps", type=str)
ap.add_argument("--GPSFile", help="GPSFile", type=str)
ap.add_argument("--latInputPoint", help="latitudeCustom", type=float)
ap.add_argument("--lonInputPoint", help="longitudeCustom", type=float)
ap.add_argument("--geoJson", help="output GeoJson", type=str)
ap.add_argument("--outputObj", help="output obj", type=str)
args = ap.parse_args()

#what method of localisation
if args.method == "auto":
    # Opening JSON file
    with open(args.GPSFile, 'r') as inputfile:
        # Reading from json file
        json_object = json.load(inputfile)
    
    latitude = json_object["latitude"]
    longitude = json_object["longitude"]

    location=(latitude, longitude)
else:
    location = (args.latitudeCustom, args.longitudeCustom)


#conversion of the longitude and latitude into tiles
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)


lat_rad, lon_deg = location[0], location[1]
zoom = 15
xtile, ytile = deg2num(lat_deg=lat_rad, lon_deg=lon_deg, zoom=zoom)

#request on OSM Buildings
url = "https://data.osmbuildings.org/0.2/anonymous/tile/{0}/{1}/{2}.json".format(zoom, xtile, ytile) 
agentheader = {'User-Agent': 'PostmanRuntime/7.28.4'}

response = requests.get(url,headers = agentheader)

data = json.loads(response.text)

#export the GeoJSON
with open(args.geoJson, 'w') as f:
  json.dump(data, f)
  
#get the polygons and heights in the GeoJSON
gdf = gpd.read_file(args.geoJson)

buildings_geojson = []
heights_geojson = []

for polygon in gdf[gdf.geometry.type == "Polygon"].geometry:
    buildings_geojson.append(Polygon(polygon.exterior.coords))
    
for height in gdf.height:
    heights_geojson.append(height)
    
#convert the coordinates for the mesh
factor = 1000
min_heights = min(heights_geojson)
max_heights = max(heights_geojson)

buildings_mesh = []
heights_2 = []

max_x, max_y = 0, 0
for i in range(len(buildings_geojson)):
    if max(buildings_geojson[i].exterior.coords.xy[0]) > max_x:
        max_x = max(buildings_geojson[i].exterior.coords.xy[0])
    if max(buildings_geojson[i].exterior.coords.xy[1]) > max_y:
        max_y = max(buildings_geojson[i].exterior.coords.xy[1])


for i in range(len(buildings_geojson)):
    tab = []
    for x, y in buildings_geojson[i].exterior.coords:
        x = x - max_x
        y = y - max_y
        x = x * factor
        y = y * factor
        x = round(x, 3)
        y = round(y, 3)
        tab.append((x, y))
    buildings_mesh.append(Polygon(tab))


for i in range(len(heights_geojson)):
    h = heights_geojson[i] / max_heights 
    heights_2.append(h)


#convert camera position the same way
position_x = location[1]
position_x -= max_x
position_x *= factor
position_x = round(position_x, 3)

position_y = location[0]
position_y -= max_y
position_y *= factor
position_y = round(position_y, 3)


#add all mesh to a scene
scene = trimesh.Scene()

for i in range(len(buildings_mesh)):
    mesh = trimesh.creation.extrude_polygon(buildings_mesh[i], heights_2[i])
    
    #relocate the mesh to align to the camera position
    mesh.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(90), [1, 0, 0]))
    mesh.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(180), [0, 0, 1]))
    mesh.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(180), [0, 1, 0]))
    mesh.apply_transform(trimesh.transformations.translation_matrix([-position_x, 0, position_y]))
    mesh.apply_transform(trimesh.transformations.scale_matrix(2))
    scene.add_geometry(mesh)


#export the Obj
with open(args.outputObj, 'w') as file:
    scene.export(
        file,
        file_type='obj',
    )
    
  #TODO si on est sur un bord de map, récupérer les maps autour, faire un paramètre