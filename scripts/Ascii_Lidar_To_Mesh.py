import numpy as np
import laspy as lp
from stl import mesh
import trimesh
import matplotlib.tri as mtri
import re

#get arguments
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("inputFile", help="input file", type=str)
ap.add_argument("MeshMethod", help="mesh method", type=str)
ap.add_argument("dist", help="dist", type=int)
ap.add_argument("ExportObj", help="Export obj", type=str)
ap.add_argument("ExportStl", help="Export stl", type=str)
args = ap.parse_args()


#import lidar file
input_file = args.inputFile


if input_file.endswith('.las'):
  point_cloud = lp.read(input_file)
  #CROP
  #store coordinates in "points"
  points = np.column_stack((point_cloud.x, point_cloud.y, point_cloud.z))
  #print("Number of points in original file:", len(points))

  bbox_percent = args.dist/2000 #if we say that a tile is 2km wide

elif input_file.endswith('.asc'):
  fichier = open(input_file, "r")
  fichier = fichier.read()
  lines = [x for x in fichier.split('\n')]

  sizeCols = lines[0]
  sizeRows = lines[1]

  path = r'^.*_(\d{1,2})M_.*$'
  result = re.search(path, input_file)

  scaleSize = int(result.group(1)) #m

  print(type(scaleSize))

  sizeCols = sizeCols.split(" ")
  sizeCols = int(sizeCols[-1:][0])

  sizeRows = sizeRows.split(" ")
  sizeRows = int(sizeRows[-1:][0])

  arraySize = sizeRows * sizeCols

  print(f"Size of array : {arraySize}")

  x_all = [None] * arraySize
  y_all = [None] * arraySize

  for i in range(arraySize):
      x_all[i] = i*scaleSize%(scaleSize*sizeCols)
      y_all[i] = (i//sizeCols)*scaleSize

  #get z data from ascii file and put it in a single array
  #each line containes 1000 values and there are 1000 lines
  ascii_grid = np.loadtxt(input_file, skiprows=6)
  z_all = ascii_grid.flatten()

  x_all = np.array(x_all)
  y_all = np.array(y_all)
  points = np.column_stack((x_all, y_all, z_all))
  args.MeshMethod = "delaunay"

  bbox_percent = args.dist/(scaleSize*1000) #if we say that a tile is 2km wide

#get boundingbox of all point cloud 
points_min = np.min(points, axis=0)
points_max = np.max(points, axis=0)
bbox_size = points_max - points_min

mean = np.mean(points, axis=0)

# print(f"min={points_min}, max={points_max}, size={bbox_size}")
# print(f"percent={bbox_percent}")

#crop bounding box and crop point cloud from mean point and bounding box size
crop_bbox = bbox_size * bbox_percent
centered_points = [p - mean for p in points]
crop_points = [p for p in centered_points if abs(p[0]) < crop_bbox[0] and abs(p[1]) < crop_bbox[1]]

# print("Points size: " + str(len(centered_points)))
# print("Crop points size: " + str(len(crop_points)))

# print("Split")
x_all, y_all, z_all = np.hsplit(np.array(crop_points), 3)
x_all = x_all.flatten()
y_all = y_all.flatten()
z_all = z_all.flatten()


if args.MeshMethod == 'voxel':
  #store coordinates cropped in crop_points
  crop_points = np.column_stack((x_all, y_all, z_all))
  print("Number of points in original file:",len(crop_points))
  #change voxel_size to vary subject resolution, it is mesured in meters
  voxel_size=1.5 #determinates the resolution of the mesh
  nb_vox=np.ceil((np.max(crop_points, axis=0) - np.min(crop_points, axis=0))/voxel_size)
  print("The voxel grid is X,Y,Z voxels:", (nb_vox))

  #reduce resolution through the voxel method
  nb_vox_readout = np.prod(nb_vox, dtype=int) 
  print("This will reduce number of points to", nb_vox_readout)

  pts_length = len(crop_points)
  perct = ((1-(nb_vox_readout/pts_length))*100)
  print("Or reduce by", perct, "%")

  #Define a function that takes as input an array of points, and a voxel size expressed in meters. It returns the sampled point cloud
  def grid_subsampling(crop_points, voxel_size):
    non_empty_voxel_keys, inverse, nb_pts_per_voxel= np.unique(((crop_points - np.min(crop_points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
    idx_pts_vox_sorted=np.argsort(inverse)
    voxel_grid={}
    grid_barycenter,grid_candidate_center=[],[]
    last_seen=0

    for idx,vox in enumerate(non_empty_voxel_keys):
      voxel_grid[tuple(vox)]=crop_points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
      grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
      grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)]-np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
      last_seen+=nb_pts_per_voxel[idx]

    return grid_candidate_center

  grid_sampled_point_cloud = grid_subsampling(crop_points, voxel_size)
  grid_sample_pc_np = np.array(grid_sampled_point_cloud)

  #Triangulation from voxel grid
  x_all = grid_sample_pc_np[:,0]
  y_all = grid_sample_pc_np[:,1]
  z_all = grid_sample_pc_np[:,2]

  tris = mtri.Triangulation(x_all, y_all)

  data = np.zeros(len(tris.triangles), dtype=mesh.Mesh.dtype)
  m = mesh.Mesh(data, remove_empty_areas=False)
  m.x[:] = x_all[tris.triangles]
  m.y[:] = z_all[tris.triangles]
  m.z[:] = -y_all[tris.triangles]

  #export stl
  m.save(args.ExportStl)

elif args.MeshMethod == "delaunay":
  #Delaunay Triangulation
  tris = mtri.Triangulation(x_all, y_all)

  #Create Mesh
  data = np.zeros(len(tris.triangles), dtype=mesh.Mesh.dtype)
  m = mesh.Mesh(data, remove_empty_areas=False)
  m.x[:] = x_all[tris.triangles]
  m.y[:] = z_all[tris.triangles]
  m.z[:] = -y_all[tris.triangles]

  #Export STL
  m.save(args.ExportStl)


myMesh = trimesh.load_mesh(args.ExportStl)

#export obj
myMesh.export(args.ExportObj)