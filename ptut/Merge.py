from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class Merge(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/merge.py {allParams}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to merge files to one File.
'''

    inputs = [
        desc.File(
            name='folder',
            label='Folder',
            description='''Folder''',
            value= "",
            uid=[0],
        ),
        desc.File(
            name='GPSFile',
            label='GPS File',
            description='''GPS file''',
            value= "",
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output folder.''',
            value= desc.Node.internalFolder,
            uid=[0],
        ),
    ]