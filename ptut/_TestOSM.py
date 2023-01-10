from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class TestOSM(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/test_OSM.py {allParams}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get an image of the localisation (like a screenshot of OpenStreetMap).
'''

    inputs = [
        desc.ChoiceParam(
            name='method',
            label='GPS coordinates method',
            description='''GPS coordinates method''',
            value="custom",
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
        desc.IntParam(
            name="dist",
            label="Distance From Input Point",
            description="Distance from input point to get image.",
            value=550,
            range=(30, 1000, 1.0), # should be more than 30, otherwise doesn't work
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
            label='Image geolocalisation',
            description='''Image geolocalisation.''',
            value= desc.Node.internalFolder + "combine.png",
            uid=[0],
        ),
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output Folder''',
            value= desc.Node.internalFolder,
            uid=[0],
        ),
    ]