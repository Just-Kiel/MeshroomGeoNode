from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

#TODO allParams instead
class Sun(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/sun.py {inputFileValue} {GPSFileValue} {outputFolderValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to display sun according to time and gps.
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
    ]

    outputs = [
        desc.File(
            name='outputPath',
            label='Output',
            description='''Output''',
            value=desc.Node.internalFolder + "result.obj",
            group = "",
            uid=[],
        ),
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output Folder''',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]
