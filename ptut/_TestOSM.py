from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc
import os
import json

class TestOSM(desc.Node):
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
                    value=51,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                ),
                desc.FloatParam(
                    name="seconds",
                    label="Seconds",
                    description="",
                    value=33.668,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                )
            ],
            name="latInputPoint",
            label="Latitude Input Point",
            description="Latitude of input point to get image.",
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
                    value=21,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                ),
                desc.FloatParam(
                    name="seconds",
                    label="Seconds",
                    description="",
                    value=8.748,
                    range=(-90.0, 90.0, 0.0001),
                    uid=[0],
                )
            ],
            name="lonInputPoint",
            label="Longitude Input Point",
            description="Longitude of input point to get image.",
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

    def processChunk(self, chunk):
        try:
            chunk.logManager.start(chunk.node.verboseLevel.value)

            fp = chunk.node.internalFolder

            if chunk.node.method.value == "custom":
                # convert degrees to decimal
                # Decimal degrees = Degrees + (Minutes/60) + (Seconds/3600)
                decLat = chunk.node.latInputPoint.value[0].value + (chunk.node.latInputPoint.value[1].value/60) + (chunk.node.latInputPoint.value[2].value/3600)
                decLon = chunk.node.lonInputPoint.value[0].value + (chunk.node.lonInputPoint.value[1].value/60) + (chunk.node.lonInputPoint.value[2].value/3600)


                os.system('python ./lib/meshroom/nodes/scripts/test_OSM.py '+ str(decLat) +' '+ str(decLon) + ' ' + fp + ' ' + str(chunk.node.dist.value))
            
            if chunk.node.method.value == "auto":

                # Opening JSON file
                with open(chunk.node.GPSFile.value, 'r') as inputfile:
                
                    # Reading from json file
                    json_object = json.load(inputfile)
                
                latitude = json_object["latitude"]
                longitude = json_object["longitude"]
                
                os.system('python ./lib/meshroom/nodes/scripts/test_OSM.py '+ str(latitude) +' '+ str(longitude) + ' ' + fp + ' ' + str(chunk.node.dist.value))

        finally:
            chunk.logManager.end()
