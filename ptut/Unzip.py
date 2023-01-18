from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc
import glob

class Unzip(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/unzip_archive.py {allParams}'

    category = 'Geolocalisation'
    documentation = '''
This node allows extract files from an archive.
'''

    inputs = [
        desc.File(
            name='Archive_to_unzip',
            label='Archive_to_unzip',
            description='''Archive_to_unzip''',
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
            label='Output Folder',
            description='''Output Folder''',
            value= desc.Node.internalFolder+'/unzip',
            uid=[0],
        ),desc.File(
            name='outputFolder',
            label='Cache Folder',
            description='''Cache Folder''',
            value= desc.Node.internalFolder,
            uid=[0],
        ),
    ]