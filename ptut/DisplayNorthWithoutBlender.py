__version__ = "1.0"

from meshroom.core import desc
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))

class DisplayNorthWithoutBlender(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/generateNorth.py {inputImageValue} {outputFolderValue}'

    category = 'Geolocalisation'
    documentation = '''
        This node display a triangle to show where the north is.
    '''
    
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