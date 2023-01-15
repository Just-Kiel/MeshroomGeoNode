__version__ = "1.0"

from meshroom.core import desc
import os.path

currentDir = os.path.dirname(os.path.abspath(__file__))

class DisplaySunWithBlender(desc.CommandLineNode):
    commandLine = '{blenderPathValue} -b --python {scriptPathValue} -- {allParams}'

    category = 'Geolocalisation'
    documentation = '''
        This node displays with the sun on the 3D viewer.
    '''

    inputs = [
        desc.File(
            name='blenderPath',
            label='Blender Path',
            description='''Path to blender executable''',
            value=os.environ.get('BLENDER',"C:/Program Files (x86)/Steam/steamapps/common/Blender/blender.exe"),
            uid=[],
            group='',
        ),
        desc.File(
            name='scriptPath',
            label='Script Path',
            description='''Path to the internal script for rendering in Blender''',
            value="./lib/meshroom/nodes/scripts/generateSunBlender.py",
            uid=[],
            group='',
        ),
    ]

    outputs = [
        desc.File(
            name='outputPath',
            label='Output',
            description='''Output''',
            value=desc.Node.internalFolder + "result.obj",
            uid=[],
        )
    ]