from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

import json

class GetAverageGPSCoordinates(desc.Node):
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
    
    print('oui c meshroom')

    def processChunk(self, chunk):
        try:
            chunk.logManager.start(chunk.node.verboseLevel.value)

            # Opening JSON file
            with open(chunk.node.inputFile.value, 'r') as inputfile:
            
                # Reading from json file
                json_object = json.load(inputfile)


            print('oui')
            #get lat long from jsonfile

            latitude = []
            latitudeRef = []
            longitude = []
            longitudeRef = []
            decLat = []
            decLon	= []
            latitudeSum = 0
            longitudeSum = 0
            

            for i in range(len(json_object["views"])):
                
                print(i)

            	#get the value of lat & long
                latitude.append(json_object["views"][i]["metadata"]["GPS:Latitude"])
                latitudeRef.append(json_object["views"][i]["metadata"]["GPS:LatitudeRef"])
                print(latitude[i])

                longitude.append(json_object["views"][i]["metadata"]["GPS:Longitude"])
                longitudeRef.append(json_object["views"][i]["metadata"]["GPS:LongitudeRef"])
                print(longitude[i])
                print(longitudeRef[i])
                
            	#get the separation between Degree, Minute, Seconde
                latPoint = [float(x) for x in latitude[i].split(", ")]
                lonPoint = [float(x) for x in longitude[i].split(", ")]
                print("ici", i)
                print(lonPoint)

            	# convert degrees to decimal
            	# Decimal degrees = Degrees + (Minutes/60) + (Seconds/3600)
             
                decLat.append(latPoint[0] + (latPoint[1]/60) + (latPoint[2]/3600))
                
                if latitudeRef[i] != "N" :
                    decLat[i]=-decLat[i]
                
                decLon.append(lonPoint[0] + (lonPoint[1]/60) + (lonPoint[2]/3600))
                
                if longitudeRef[i] != "E" :
                    decLon[i] = -decLon[i]
                
                print("la", i)
                print(decLon)
                
            print(decLat[0])


            for i in range(len(latitude)):
                latitudeSum += decLat[i]
            
            for i in range(len(longitude)):
                longitudeSum += decLon[i]
                
                
            latitudeAvg = latitudeSum / len(latitude)
            longitudeAvg = longitudeSum / len(longitude)


            # Data to be written
            output = {
                "latitudeMoy": latitudeAvg,
                "longitudeMoy": longitudeAvg
            }

            # Serializing json
            json_object = json.dumps(output, indent=4)
            
            # Writing to sample.json
            with open(chunk.node.output.value, "w") as outfile:
                outfile.write(json_object)

        finally:
            chunk.logManager.end()
