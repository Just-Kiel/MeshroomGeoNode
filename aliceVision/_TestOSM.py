from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc
import os

# import sys
# print(sys.path)
# sys.path.append('C:\\Users\\Aurore\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages')
# print(sys.path)

# need this !
# import osmnx

class TestOSM(desc.Node):
    category = 'Geolocalisation'
    documentation = '''
This node allows to get an image of the localisation (like a screenshot of OpenStreetMap).
'''

    inputs = [
        desc.GroupAttribute(
            groupDesc = [
                desc.FloatParam(
                    name="degrees",
                    label="Degrees",
                    description="",
                    value=48,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                ),
                desc.FloatParam(
                    name="minutes",
                    label="Minutes",
                    description="",
                    value=50,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                ),
                desc.FloatParam(
                    name="seconds",
                    label="Seconds",
                    description="",
                    value=31.376,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                )
            ],
            name="latInputPoint",
            label="Latitude Input Point",
            description="Latitude of input point to get image.",
            # value=48.8420489,
            # range=(-90.0, 90.0, 0.0001),
        ),
        desc.GroupAttribute(
            groupDesc = [
                desc.FloatParam(
                    name="degrees",
                    label="Degrees",
                    description="",
                    value=2,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                ),
                desc.FloatParam(
                    name="minutes",
                    label="Minutes",
                    description="",
                    value=37,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                ),
                desc.FloatParam(
                    name="seconds",
                    label="Seconds",
                    description="",
                    value=22.574,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                )
            ],
            name="lonInputPoint",
            label="Longitude Input Point",
            description="Longitude of input point to get image.",
            # value=2.6229377,
            # range=(-180.0, 180.0, 0.0001),
            # uid=[0],
        ),
        desc.IntParam(
            name="dist",
            label="Distance From Input Point",
            description="Distance from input point to get image.",
            value=550,
            range=(30, 1000, 1.0),
            uid=[0],
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='''verbosity level (critical, error, warning, info, debug).''',
            value='debug',
            values=['critical', 'error', 'warning', 'info', 'debug'],
            exclusive=True,
            uid=[],
            ),
        ]

    def processChunk(self, chunk):
        try:
            chunk.logManager.start(chunk.node.verboseLevel.value)

            fp = chunk.node.internalFolder

            # convert degrees to decimal
            # Decimal degrees = Degrees + (Minutes/60) + (Seconds/3600)
            decLat = chunk.node.latInputPoint.value[0].value + (chunk.node.latInputPoint.value[1].value/60) + (chunk.node.latInputPoint.value[2].value/3600)

            print(decLat)

            decLon = chunk.node.lonInputPoint.value[0].value + (chunk.node.lonInputPoint.value[1].value/60) + (chunk.node.lonInputPoint.value[2].value/3600)

            print(decLon)

            os.system('python ./lib/meshroom/nodes/scripts/test_OSM.py '+ str(decLat) +' '+ str(decLon) + ' ' + fp + ' ' + str(chunk.node.dist.value))
            # os.system('python ./lib/meshroom/nodes/scripts/test_OSM.py '+ str(chunk.node.latInputPoint.value) +' '+ str(chunk.node.lonInputPoint.value) + ' ' + fp + ' ' + str(chunk.node.dist.value))

        finally:
            chunk.logManager.end()
