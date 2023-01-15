__version__ = "1.0"

from meshroom.core import desc

class Display2DMapWithoutBlender(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/generatePlane.py {inputImageValue} {outputFolderValue}'

    category = 'Geolocalisation'
    documentation = '''
        This node display with the 2D map image, a plane with it on the 3D viewer.
    '''
    
# TODO here idk why, but the export object is a plane but when displayed in Meshroom, it only displays half of the plane

    inputs = [
        desc.File(
            name='inputImage',
            label='InputImage',
            description='''Input image''',
            value='',
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