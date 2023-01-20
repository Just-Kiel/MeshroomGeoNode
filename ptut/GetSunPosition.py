from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class GetSunPosition(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/sunPosition.py {methodValue} {GPSFileValue} {latInputPointValue} {lonInputPointValue} {timeFileValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get position (to display in 3D viewer then) of the sun.
'''

    inputs = [
        desc.ChoiceParam(
            name='method',
            label='GPS coordinates method',
            description='''GPS coordinates method''',
            value="auto",
            values=("custom", "auto"),
            exclusive=True,
            uid=[0],
        ),
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file''',
            value= "",
            uid=[0],
        ),
        desc.FloatParam(
            name="latInputPoint",
            label="Latitude Input Point",
            description="Latitude of input point to get image.",
            value=33.668,
            range=(-180.0, 180.0, 0.0001),
            uid=[0],
        ),
        desc.FloatParam(
            name="lonInputPoint",
            label="Longitude Input Point",
            description="Longitude of input point to get image.",
            value=8.748,
            range=(-90.0, 90.0, 0.0001),
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
            label='Output',
            description='''Output.''',
            value= desc.Node.internalFolder + "sunPosition.json",
            uid=[0],
        ),
    ]