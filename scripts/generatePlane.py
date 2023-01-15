import argparse
from pathlib import Path
import trimesh
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("texturePath", help="texture path", type=Path)
ap.add_argument("exportFolderName", help="exportFolderName", type=str)
args = ap.parse_args()
texturePath = Path(args.texturePath).resolve()

parentPath = Path(__file__).parent.resolve()
outputFolderPath = parentPath / args.exportFolderName

outputFolderPath.mkdir( exist_ok=True)
objPath = outputFolderPath / 'result.obj'
mtlPath = outputFolderPath / 'mltFile.mtl'

image = Image.open(texturePath)

# create plane
plane = trimesh.Trimesh(
    vertices=[[-1, 0, 1], [1, 0, 1], [1, 0, -1], [-1, 0, -1]],
    faces=[[0, 1, 2], [0, 2, 3]],
)

# assign material using texture and uv coordinates
plane.visual = trimesh.visual.texture.TextureVisuals(uv=[[0,0], [1,0], [1, 1], [0, 1]], image=image)
plane.visual.material.name = "mapMat"

with open(objPath, 'w') as file:
    plane.export(
        file,
        file_type='obj',
        include_texture=True,
        mtl_name=mtlPath.name,
        resolver=trimesh.visual.resolvers.FilePathResolver(mtlPath)
    )