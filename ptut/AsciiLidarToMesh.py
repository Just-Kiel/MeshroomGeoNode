from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class AsciiLidarToMesh(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/Ascii_Lidar_To_Mesh.py {LidarFileValue} {LambertFileValue} {MeshMethodValue} {distValue} {outputobjValue} {outputstlValue}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to get an image of the localisation (like a screenshot of OpenStreetMap).
'''

    inputs = [
        desc.File(
            name='LidarFile',
            label='Lidar file',
            description='''Lidar file''',
            value= "",
            uid=[0],
        ),
        desc.File(
            name='LambertFile',
            label='Lambert coordinates file',
            description='''Lambert coordinates file''',
            value= "",
            uid=[0],
        ),
        desc.ChoiceParam(
            name='MeshMethod',
            label='Mesh method',
            description='''Mesh Method (Voxel, Delaunay Triangulation).''',
            value='voxel',
            values=['voxel', 'delaunay'],
            exclusive=True,
            uid=[],
            group="",
            ),
        desc.IntParam(
            name="dist",
            label="Distance From Center (m)",
            description="Distance from center point (m)",
            value=200,
            range=(50, 2000, 1.0), # should be more than 30, otherwise doesn't work
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
            group="",
            ),
    ]

    outputs = [
        desc.File(
            name='outputobj',
            label='OBJ from Lidar',
            description='''OBJ from Lidar''',
            value= desc.Node.internalFolder + "mesh.obj",
            uid=[0],
        ),
        desc.File(
            name='outputstl',
            label='STL from Lidar',
            description='''STL from Lidar''',
            value= desc.Node.internalFolder + "mesh.stl",
            uid=[0],
        ),
    ]