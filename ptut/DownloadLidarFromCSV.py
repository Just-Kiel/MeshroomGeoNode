from __future__ import print_function
import glob

__version__ = "1.2"

from meshroom.core import desc

class DownloadLidarFromCSV(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/downloadLidarFromCSV.py {Lambert93FileValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get position (to display in 3D viewer then) of the sun.
'''

    inputs = [
        desc.File(
            name='Lambert93File',
            label='Lambert93 coordinates file',
            description='''GPS coordinates file''',
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
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='output',
            label='Output',
            description='''Output.''',
            value= desc.Node.internalFolder,
            # value= glob.glob(desc.Node.internalFolder+"/*.7z"),
            uid=[0],
        ),
    ]