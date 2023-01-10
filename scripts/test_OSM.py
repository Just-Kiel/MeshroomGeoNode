import osmnx as ox

from PIL import ImageChops
from PIL import Image
import sys
import json

# configure the inline image display
extension = "png"
size = 600
dpi = 300

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


#### Get roads layer
fp = path + f"roads.{extension}"
roads = ox.plot_figure_ground(
    point=point,
    network_type="all",
    default_width=3.3,
    filepath=fp,
    dpi=dpi,
    save=True,
    show=False,
    dist= dist
)


fp = path + f"buildings.{extension}"
#### Get buildings layer
tags = {"amenity": True, "building":True}
gdf = ox.geometries_from_point(point, tags, dist=dist)
buildings = ox.plot_footprints(
    gdf,
    save=True,
    filepath=fp,
    show=False,
    dpi=dpi
)

buildings = path + f"buildings.{extension}"
roads = path + f"roads.{extension}"

image1 = Image.open(buildings)
image2 = Image.open(roads)

# resize image before cropping the other one
ratio = image2.width / image2.height
new_height = 1590
new_width = int(ratio * new_height)

image2 = image2.resize((new_width, new_height))
image2.save(roads)
image2 = Image.open(roads)

# cropping image
crop_size = ((image1.width - image2.width)/2, 0,image2.width + ((image1.width - image2.width)/2), image1.height)
image1 = image1.crop(crop_size)
image1.save(buildings)
image1 = Image.open(buildings)


# merging of 2 images (layers)
image3 = ImageChops.add(image2, image1)
image3 = image3.save(finalFp)