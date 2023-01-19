# TODO try to x, y with 25 ++ and z with tab data

# TODO à tester
# import numpy as np
# import laspy

# # Read the ESRI ASCII grid file
# data = np.loadtxt("file.asc", skiprows=6)

# # Create a new LAS file
# outfile = laspy.file.File("file.las", mode="w", header=laspy.header.Header())

# # Add the data from the ESRI ASCII grid file to the LAS file
# outfile.X = np.arange(data.shape[1])
# outfile.Y = np.arange(data.shape[0])
# outfile.Z = data

# # Close the LAS file
# outfile.close()

import numpy as np
import laspy as lp
from stl import mesh
import trimesh
import matplotlib.tri as mtri

#import lidar file
asc_file = "D:/PTUT/oli/MeshroomCache/Unzip/df5e7c7fa887e72ef65bafbe7798558569b6fa4c/unzip/RGEALTI/1_DONNEES_LIVRAISON_2021-10-00009/RGEALTI_MNT_5M_ASC_LAMB93_IGN69_D093/RGEALTI_FXX_0645_6870_MNT_LAMB93_IGN69.asc"
# asc_file = "D:/PTUT/oli/MeshroomCache/Unzip/38dfeb28e0601bc0ac2131ee9185a4cfd77ee17b/unzip/BDALTIV2/1_DONNEES_LIVRAISON_2021-10-00008/BDALTIV2_MNT_25M_ASC_LAMB93_IGN69_D093/BDALTIV2_25M_FXX_0625_6875_MNT_LAMB93_IGN69.asc"

fichier = open(asc_file, "r")
fichier = fichier.read()

lines = [x for x in fichier.split('\n')]

sizeCols = lines[0]
sizeRows = lines[1]
scaleSize = 1 #m

sizeCols = sizeCols.split(" ")
sizeCols = int(sizeCols[-1:][0])

sizeRows = sizeRows.split(" ")
sizeRows = int(sizeRows[-1:][0])

arraySize = sizeRows * sizeCols

print(f"Size of array : {arraySize}")

lines = lines[6:-1]
# print(lines)


x_all = [None] * arraySize
y_all = [None] * arraySize

for i in range(arraySize):
    x_all[i] = i*scaleSize%(scaleSize*sizeCols)
    y_all[i] = (i//sizeCols)*scaleSize

# print(x_points)
# print(y_points[1000])

#get z data from ascii file and put it in a single array
#each line containes 1000 values and there are 1000 lines
ascii_grid = np.loadtxt(asc_file, skiprows=6)
z_all = ascii_grid.flatten()

print(f"lignes : {z_all}")
print(z_all[2000])

print(len(z_all))

points = np.column_stack((x_all, y_all, z_all))

x_all = np.array(x_all)
y_all = np.array(y_all)

print(f"array_points : {points}")
print(f"x_points : {x_all}")
# print(f"z_points : {type(z_all[0])}")
# exit(0)


#Delaunay Triangulation
tris = mtri.Triangulation(x_all, y_all)

#Create Mesh
data = np.zeros(len(tris.triangles), dtype=mesh.Mesh.dtype)
m = mesh.Mesh(data, remove_empty_areas=False)
m.x[:] = x_all[tris.triangles]
m.y[:] = y_all[tris.triangles]
m.z[:] = z_all[tris.triangles]

# exportPath = "D:/PTUT/oli/MeshroomCache/Unzip/38dfeb28e0601bc0ac2131ee9185a4cfd77ee17b/unzip/BDALTIV2/1_DONNEES_LIVRAISON_2021-10-00008/BDALTIV2_MNT_25M_ASC_LAMB93_IGN69_D093/objet.stl"
exportPath = "D:/PTUT/oli/MeshroomCache/Unzip/df5e7c7fa887e72ef65bafbe7798558569b6fa4c/unzip/RGEALTI/1_DONNEES_LIVRAISON_2021-10-00009/RGEALTI_MNT_5M_ASC_LAMB93_IGN69_D093/objet.stl"
#Export STL
m.save(exportPath)