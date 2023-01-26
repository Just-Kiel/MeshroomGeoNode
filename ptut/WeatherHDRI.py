from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

#TODO allParams instead
class WeatherHDRI(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/weatherHDRI.py {inputFileValue} {GPSFileValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get an HDRI file according to the weather at moment of dataset.
'''

    inputs = [
        desc.File(
            name='inputFile',
            label='SfMData',
            description='''input SfMData.''',
            value= "",
            uid=[0],
        ),
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
            label='Hdri result',
            description='hdri from weather folder',
            value=desc.Node.internalFolder+'hdri.exr',
            uid=[],
        ),
    ]
