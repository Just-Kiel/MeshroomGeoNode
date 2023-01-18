from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class ConvertLAZtoLAS(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/LAZtoLAS.py {LAZFolderValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to convert Laz files to Las Files.
'''

    inputs = [
        desc.File(
            name='LAZFolder',
            label='LAZ Folder',
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
            value= desc.Node.internalFolder,
            uid=[0],
        ),
    ]