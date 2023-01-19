import argparse
from pathlib import Path
import trimesh
import numpy as np
from PIL import Image
import json


ap = argparse.ArgumentParser()
ap.add_argument("inputImage", help="inputImage", type=str)
ap.add_argument("exportFolderName", help="exportFolderName", type=str)
args = ap.parse_args()
texturePath = Path(args.inputImage).resolve()

parentPath = Path(__file__).parent.resolve()
outputFolderPath = parentPath / args.exportFolderName

outputFolderPath.mkdir( exist_ok=True)
objPath = outputFolderPath / 'result.obj'
mtlPath = outputFolderPath / 'texture.mtl'

image = Image.open(texturePath)



triangle = trimesh.creation.cone(0.5, 2)

angle = np.deg2rad(180)
axis = [0, 1, 0]
rotation_matrix = trimesh.transformations.rotation_matrix(angle, axis)
translation_matrix = trimesh.transformations.translation_matrix([0, 0, -6])

triangle.apply_transform(rotation_matrix)
triangle.apply_transform(translation_matrix)

triangle.visual = trimesh.visual.texture.TextureVisuals(image=image)
triangle.visual.material.name = "mapMat"



with open(objPath, 'w') as file:
    triangle.export(
        file,
        file_type='obj',
        include_texture=True,
        mtl_name=mtlPath.name,
        resolver=trimesh.visual.resolvers.FilePathResolver(mtlPath)
    )

