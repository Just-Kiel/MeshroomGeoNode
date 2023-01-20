from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class SRTMDataTo3D(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/DEMto3DFULL.py {allParams}'

    category = 'Geolocalisation'

    documentation = '''
This node allows to get SRTM Data represented as a mesh of the localisation.
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
        desc.FloatParam(
            name="kilometers",
            label="Bounding Box in kilometers",
            description="Bounding Box in kilometers",
            value=100,
            range=(1, 1000),
            uid=[0],
        ),
        desc.FloatParam(
            name="scale",
            label="Scale",
            description="Scale of the map",
            value=0.2,
            range=(0, 1),
            uid=[0],
        ),
        desc.FloatParam(
            name="verticalTranslation",
            label="Vertical translation",
            description="Vertical translation",
            value=10,
            range=(-100, 100),
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
            value= desc.Node.internalFolder + "result.obj",
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