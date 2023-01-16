import bpy
import os
import sys

argv = sys.argv
argv = [element if "--" not in element else "" for element in argv]
argv = [x for x in argv if x != ""]

imagePath = argv[3]
outputPath = argv[4]


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


def new_plane(mylocation, mysize, myname):
    bpy.ops.mesh.primitive_plane_add(
        size=mysize,
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=mylocation,
        rotation=(0, 0, 0),
        scale=(0, 0, 0))
    current_name = bpy.context.selected_objects[0].name
    plane = bpy.data.objects[current_name]
    plane.name = myname
    plane.data.name = myname + "_mesh"
    return

new_plane((0,0,-1), 10, "MyFloor")

mat = bpy.data.materials.new(name="New_Mat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
texImage.image = bpy.data.images.load(imagePath)
mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

ob = bpy.data.objects['MyFloor']

if len(ob.data.materials.items()) != 0:
    ob.data.materials.clear()
else:
    ob.data.materials.append(mat)
    
blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
target_file = os.path.join(directory, outputPath)

bpy.ops.export_scene.obj(filepath=target_file)