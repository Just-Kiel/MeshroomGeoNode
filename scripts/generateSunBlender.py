import bpy
import os
import sys
import math

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

new_sphere((0,0.15,15), 1, "MySun")

sun = bpy.context.object

sun.rotation_euler = [0, 0, math.radians(181)]

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
    
blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
target_file = os.path.join(directory, 'pouic.obj')

bpy.ops.export_scene.obj(filepath=target_file)