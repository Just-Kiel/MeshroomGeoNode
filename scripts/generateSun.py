from pathlib import Path
import trimesh
import numpy as np
from PIL import Image
import json

def generateSun(output, sunData):
    path = "./lib/meshroom/nodes/scripts/yellow_texture.jpg"
    texturePath = Path(path).resolve()

    parentPath = Path(__file__).parent.resolve()
    outputFolderPath = parentPath / output

    outputFolderPath.mkdir( exist_ok=True)
    objPath = outputFolderPath / 'result.obj'
    mtlPath = outputFolderPath / 'texture.mtl'

    print(outputFolderPath)

    image = Image.open(texturePath)

    # Y = floor distance
    # Z = sun earth distance
    # rotate(azimuth)

    # Reading from json file
    json_object = json.loads(sunData)

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

    with open(objPath, 'w') as file:
        sphere.export(
            file,
            file_type='obj',
            include_texture=True,
            mtl_name=mtlPath.name,
            resolver=trimesh.visual.resolvers.FilePathResolver(mtlPath)
        )