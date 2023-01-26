from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class Map3D(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/map3D.py {allParams}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get 3D map of where is the dataset.
'''

    inputs = [
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file.''',
            value= "",
            uid=[0],
        ),
        desc.ChoiceParam(
            name='resolution',
            label='Resolution (meters)',
            description='''Resolution of the mesh.''',
            value=25,
            values=[0.30, 1, 5, 25],
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output Folder''',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]
