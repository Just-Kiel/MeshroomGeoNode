from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

import json

class GetHdriFromWeather(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/get_hdri.py {weatherFileValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get time of dataset.
'''

    inputs = [
        desc.File(
            name='weatherFile',
            label='weather File',
            description='''weather file.''',
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
            label='Hdri result',
            description='hdri from weather file',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]