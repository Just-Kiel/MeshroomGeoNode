from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

#TODO allParams instead
class Map2D(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/map2D.py {GPSFileValue} {distValue} {outputPathValue} {outputFolderValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get 2D map of where is the dataset.
'''

    inputs = [
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file.''',
            value= "",
            uid=[0],
        ),
        desc.IntParam(
            name="dist",
            label="Distance From Input Point",
            description="Distance from input point to get image.",
            value=550,
            range=(30, 1000, 1.0), # should be more than 30, otherwise doesn't work
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='outputPath',
            label='Output',
            description='''Output''',
            value=desc.Node.internalFolder + "map2D.obj",
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
