from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class MergeLAS(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/merge.py {LASFolderValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to merge Las files to one Las File.
'''

    inputs = [
        desc.File(
            name='LASFolder',
            label='LAS Folder',
            description='''LAZ folder''',
            value= "",
            uid=[0],
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='''verbosity level (critical, error, warning, info, debug).''',
            value='info',
            values=['critical', 'error', 'warning', 'info', 'debug'],
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name='output',
            label='Output',
            description='''Output.''',
            value= desc.Node.internalFolder+"result.las",
            uid=[0],
        ),
    ]