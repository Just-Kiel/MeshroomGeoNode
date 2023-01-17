from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc
import json

class GetGPSCoordinates(desc.Node):
    category = 'Geolocalisation'
    documentation = '''
This node allows to get GPS coordinates of a file.
'''

    inputs = [
        desc.File(
            name='inputFile',
            label='SfMData',
            description='''input SfMData.''',
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
            label='GPS coordinates',
            description='GPS coordinates from input file',
            value=desc.Node.internalFolder + "gps.json",
            uid=[],
        ),
    ]

    def processChunk(self, chunk):
        try:
            chunk.logManager.start(chunk.node.verboseLevel.value)

            # Opening JSON file
            with open(chunk.node.inputFile.value, 'r') as inputfile:
            
                # Reading from json file
                json_object = json.load(inputfile)

            latitude = json_object["views"][0]["metadata"]["GPS:Latitude"]
            latitudeRef = json_object["views"][0]["metadata"]["GPS:LatitudeRef"]

            longitude = json_object["views"][0]["metadata"]["GPS:Longitude"]
            longitudeRef = json_object["views"][0]["metadata"]["GPS:LongitudeRef"]
        
            latPoint = [float(x) for x in latitude.split(", ")]
            lonPoint = [float(x) for x in longitude.split(", ")]

            # convert degrees to decimal
            # Decimal degrees = Degrees + (Minutes/60) + (Seconds/3600)
            decLat = latPoint[0] + (latPoint[1]/60) + (latPoint[2]/3600)
            decLat = decLat if latitudeRef == "N" else -decLat

            decLon = lonPoint[0] + (lonPoint[1]/60) + (lonPoint[2]/3600)
            decLon = decLon if longitudeRef == "E" else -decLon

            # Data to be written
            output = {
                "latitude": decLat,
                "longitude": decLon
            }

            # Serializing json
            json_object = json.dumps(output, indent=4)
            
            # Writing to sample.json
            with open(chunk.node.output.value, "w") as outfile:
                outfile.write(json_object)

        finally:
            chunk.logManager.end()
