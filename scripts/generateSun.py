import argparse
from pathlib import Path
import trimesh
import numpy as np
from PIL import Image
import json

ap = argparse.ArgumentParser()
ap.add_argument("inputImage", help="inputImage", type=str)
ap.add_argument("exportFolderName", help="exportFolderName", type=str)
ap.add_argument("sunPositionFile", help="sunPositionFile", type=str)
args = ap.parse_args()
texturePath = Path(args.inputImage).resolve()

parentPath = Path(__file__).parent.resolve()
outputFolderPath = parentPath / args.exportFolderName

outputFolderPath.mkdir( exist_ok=True)
objPath = outputFolderPath / 'result.obj'
mtlPath = outputFolderPath / 'texture.mtl'

image = Image.open(texturePath)

# Y = floor distance
# Z = sun earth distance
# rotate(azimuth)

with open(args.sunPositionFile, 'r') as inputfile:
    # Reading from json file
    json_object = json.load(inputfile)

offsetY = json_object["heightFromSun"]
offsetZ = json_object["earthSun"]
rotation = json_object["azimuth"]

# create plane
sphere = trimesh.creation.uv_sphere(5)

# Define the point you want to rotate the sphere around
rotation_point = [offsetY, offsetZ, 0]

# Define the angle of rotation (in radians)
angle = np.deg2rad(rotation)

# Define the axis of rotation
axis = [0, 1, 0]

# Create a translation matrix to move the sphere to the point of rotation
translation_matrix = trimesh.transformations.translation_matrix(rotation_point)

# Create a rotation matrix
rotation_matrix = trimesh.transformations.rotation_matrix(angle, axis)

# Create a translation matrix to move the sphere back to the original position
translation_matrix_back = trimesh.transformations.translation_matrix(rotation_point)

# Apply the translation matrix to the sphere
sphere.apply_transform(translation_matrix)

# Apply the rotation matrix to the sphere
sphere.apply_transform(rotation_matrix)

# assign material using texture and uv coordinates
sphere.visual = trimesh.visual.texture.TextureVisuals(image=image)
sphere.visual.material.name = "mapMat"

# display test
# scene = trimesh.Scene()
# scene.add_geometry(plane)
# scene.add_geometry(trimesh.creation.axis())
# scene.show()

with open(objPath, 'w') as file:
    sphere.export(
        file,
        file_type='obj',
        include_texture=True,
        mtl_name=mtlPath.name,
        resolver=trimesh.visual.resolvers.FilePathResolver(mtlPath)
    )