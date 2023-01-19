from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class DownloadScan3dFromCSV(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/download_scan3d_from_CSV.py {DepartementFileValue} {Scan3dTypeValue} {outputValue}'

    category = 'Geolocalisation'
    documentation = '''
'''

    inputs = [
        desc.File(
            name='DepartementFile',
            label='Departement file',
            description='''Departement file''',
            value= "",
            uid=[0],
        ),
        desc.ChoiceParam(
            name='Scan3dType',
            label='Scan3d Type',
            description='''Scan3d Type (1m, 5m, 25m).''',
            value='1m',
            values=['1m', '5m', '25m'],
            exclusive=True,
            uid=[0],
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='''verbosity level (critical, error, warning, info, debug).''',
            value='info',
            values=['critical', 'error', 'warning', 'info', 'debug'],
            exclusive=True,
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='output',
            label='Output',
            description='''Output.''',
            value= desc.Node.internalFolder,
            uid=[0],
        ),
    ]