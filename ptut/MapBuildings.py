__version__ = "1.0"

from meshroom.core import desc

class MapBuildings(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/OSMBuildings.py {methodValue} {gpsFileValue} {latInputPointValue} {lonInputPointValue} {outputObjValue} {geoJsonValue}'

    category = 'Geolocalisation'
    documentation = '''
        This node display the 2,5D Map with OSM Buildings data.
    '''
    
    inputs = [
        desc.ChoiceParam(
            name='method',
            label='GPS Coordinates Method',
            description='''GPS coordinates method''',
            value="custom",
            values=("custom", "auto"),
            exclusive=True,
            uid=[0],
        ),
        desc.File(
            name='gpsFile',
            label='GPS Coordinates File',
            description='''GPS coordinates file''',
            value= "",
            uid=[0],
        ),
        desc.FloatParam(
            name="latInputPoint",
            label="Latitude Input Point",
            description="Latitude of input point.",
            value=48.85864742340504, 
            range=(-180.0, 180.0, 0.0001),
            uid=[0],
        ),
        desc.FloatParam(
            name="lonInputPoint",
            label="Longitude Input Point",
            description="Longitude of input point.",
            value=2.3520693092219593,
            range=(-90.0, 90.0, 0.0001),
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='geoJson',
            label='GeoJSON',
            description='''GeoJSON.''',
            value= desc.Node.internalFolder + "geojson.geojson",
            uid=[0],
        ),
        desc.File(
            name='outputObj',
            label='Output Obj',
            description='''Output''',
            value=desc.Node.internalFolder + "result.obj",
            group = "",
            uid=[],
        ),
    ]