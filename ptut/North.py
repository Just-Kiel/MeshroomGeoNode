from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

#TODO allParams instead
class North(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/north.py {GPSFileValue} {outputPathValue} {outputFolderValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get north around dataset.
'''

    inputs = [
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file.''',
            value= "",
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='outputPath',
            label='Output',
            description='''Output''',
            value=desc.Node.internalFolder + "north.obj",
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
