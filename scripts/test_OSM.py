import osmnx as ox

from PIL import ImageChops
from PIL import Image
import sys

# configure the inline image display
extension = "png"
size = 600
dpi = 300

point = (float(sys.argv[1]), float(sys.argv[2]))
dist = int(sys.argv[4])

#### Get roads layer
fp = sys.argv[3] + f"roads.{extension}"
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


fp = sys.argv[3] + f"buildings.{extension}"
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

buildings = sys.argv[3] + f"buildings.{extension}"
roads = sys.argv[3] + f"roads.{extension}"

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
image3 = image3.save(sys.argv[3] + f"combine.{extension}")