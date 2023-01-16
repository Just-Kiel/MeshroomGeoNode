__version__ = "1.0"

from meshroom.core import desc

class DisplaySunWithoutBlender(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/generateSun.py {inputImageValue} {outputFolderValue} {sunPositionFileValue}'

    category = 'Geolocalisation'
    documentation = '''
        This node display with the 2D map image, a plane with it on the 3D viewer.
    '''
    

    inputs = [
        desc.File(
            name='inputImage',
            label='InputImage',
            description='''Input image''',
            value='./lib/meshroom/nodes/scripts/yellow_texture.jpg',
            uid=[0],
        ),
        desc.File(
            name='sunPositionFile',
            label='Sun position file Path',
            description='''Sun position file Path''',
            value="",
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='outputPath',
            label='Output',
            description='''Output''',
            value=desc.Node.internalFolder + "result.obj",
            group = "",
            uid=[],
        ),
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output Folder''',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]