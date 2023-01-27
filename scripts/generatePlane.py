from pathlib import Path
import trimesh
from PIL import Image

def generatePlane(TexturePath, OutputFolder, Output):
    texturePath = Path(TexturePath).resolve()

    parentPath = Path(__file__).parent.resolve()
    outputFolderPath = parentPath / OutputFolder

    outputFolderPath.mkdir( exist_ok=True)
    objPath = Output
    mtlPath = outputFolderPath / 'mltFile.mtl'

    image = Image.open(texturePath)

    # create plane
    plane = trimesh.Trimesh(
        vertices=[[-15, 0, 15], [15, 0, 15], [15, 0, -15], [-15, 0, -15]],
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

    #force add line to .obj because assimp doesn't read last line so miss a face
    file = open(objPath, 'a+')
    file.write('\n')
    file.close()