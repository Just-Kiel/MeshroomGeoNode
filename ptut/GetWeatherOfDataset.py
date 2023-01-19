from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc


class GetWeatherOfDataset(desc.CommandLineNode):

    commandLine = 'python ./lib/meshroom/nodes/scripts/get_weather.py {GPSFileValue} {timeFileValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get the weather of dataset.
'''

    inputs = [
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file''',
            value= "",
            uid=[0],
        ),
        desc.File(
            name="timeFile",
            label="Time from file",
            description="Time from file.",
            value="",
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
            label='Weather result',
            description='Weather from dataset',
            value=desc.Node.internalFolder + "weatherDataset.json",
            uid=[],
        ),
    ]