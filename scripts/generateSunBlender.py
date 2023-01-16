import bpy
import math
import sys
import json

# get arguments
argv = sys.argv
argv = [element if "--" not in element else "" for element in argv]
argv = [x for x in argv if x != ""]

sunPositionFile = argv[3]
outputFile = argv[4]

with open(sunPositionFile, 'r') as inputfile:
    # Reading from json file
    json_object = json.load(inputfile)

offsetY = json_object["heightFromSun"]
offsetZ = json_object["earthSun"]
rotation = json_object["azimuth"]

# Y = floor distance
# Z = sun earth distance
# rotate(azimuth)

try:
    camera = bpy.data.objects['Camera']
    light = bpy.data.objects['Light']
    cube = bpy.data.objects['Cube']
    bpy.data.objects.remove(cube, do_unlink=True)
    bpy.data.objects.remove(camera, do_unlink=True)
    bpy.data.objects.remove(light, do_unlink=True)
except:
    print("Object bpy.data.objects['Cube'] not found")
    
bpy.ops.outliner.orphans_purge()


def new_sphere(mylocation, mysize, myname):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=mysize,
        enter_editmode=False,
        align='WORLD',
        location = mylocation
        )
    current_name = bpy.context.selected_objects[0].name
    plane = bpy.data.objects[current_name]
    plane.name = myname
    plane.data.name = myname + "_mesh"
    return

new_sphere((0,offsetY,offsetZ), 10, "MySun")

sun = bpy.context.object

bpy.ops.transform.rotate(value=math.radians(rotation), orient_axis='Z', center_override=(0,0,0))

sun.data.polygons.foreach_set('use_smooth',  [True] * len(sun.data.polygons))


mat = bpy.data.materials.new(name="Sun_Mat")
mat.use_nodes = True

bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (1, 0.9, 0.3, 1)

sun = bpy.data.objects['MySun']

if len(sun.data.materials.items()) != 0:
    sun.data.materials.clear()
else:
    sun.data.materials.append(mat)
    
target_file = outputFile

bpy.ops.export_scene.obj(filepath=target_file)