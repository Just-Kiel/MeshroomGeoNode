from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

import json

class GetTimeOfDataset(desc.Node):
    category = 'Geolocalisation'
    documentation = '''
This node allows to get time of dataset.
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
            label='Time result',
            description='Time from input file',
            value=desc.Node.internalFolder + "time.json",
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

            datetime = json_object["views"][0]["metadata"]["Exif:DateTimeOriginal"]
            offsetTime = json_object["views"][0]["metadata"]["Exif:OffsetTimeOriginal"]

            offsetTime = offsetTime.replace(":", ".")
            offsetTime = int(float(offsetTime))

            datetime = datetime.replace(" ", ":")

            datetime = [x for x in datetime.split(":")]

            # Data to be written
            output = {
                "datetime": datetime,
                "offsetTime": offsetTime
            }

            # Serializing json
            json_object = json.dumps(output, indent=4)
            
            # Writing to sample.json
            with open(chunk.node.output.value, "w") as outfile:
                outfile.write(json_object)

        finally:
            chunk.logManager.end()
