from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class GetRegion(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/getRegion.py {GPSFileValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get region of dataset.
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
            label='Region result',
            description='Region from input file',
            value=desc.Node.internalFolder + "region.json",
            uid=[],
        ),
    ]