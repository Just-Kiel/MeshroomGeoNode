import numpy as np
import laspy as lp
from stl import mesh
import trimesh

#get arguments
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("LidarFile", help="lidar file", type=str)
ap.add_argument("ExportObj", help="Export obj", type=str)
ap.add_argument("ExportStl", help="Export stl", type=str)
args = ap.parse_args()

#import lidar file
lidar_file = args.LidarFile
point_cloud = lp.read(lidar_file)

#store coordinates in "points"
points = np.vstack((point_cloud.x, point_cloud.y, point_cloud.z)).transpose()
print("Number of points in original file:",len(points))

#change voxel_size to vary subject resolution, it is mesured in meters
voxel_size=2
nb_vox=np.ceil((np.max(points, axis=0) - np.min(points, axis=0))/voxel_size)
print("The voxel grid is X,Y,Z voxels:", (nb_vox))

#reduce resolution through the voxel method
nb_vox_readout = np.prod(nb_vox, dtype=int) 
print("This will reduce number of points to", nb_vox_readout)

pts_length = len(points)
perct = ((1-(nb_vox_readout/pts_length))*100)
print("Or reduce by", perct, "%")

#Define a function that takes as input an array of points, and a voxel size expressed in meters. It returns the sampled point cloud
def grid_subsampling(points, voxel_size):

#   nb_vox=np.ceil((np.max(points, axis=0) - np.min(points, axis=0))/voxel_size)
  non_empty_voxel_keys, inverse, nb_pts_per_voxel= np.unique(((points - np.min(points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
  idx_pts_vox_sorted=np.argsort(inverse)
  voxel_grid={}
  grid_barycenter,grid_candidate_center=[],[]
  last_seen=0

  for idx,vox in enumerate(non_empty_voxel_keys):
    voxel_grid[tuple(vox)]=points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
    grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
    grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)]-np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
    last_seen+=nb_pts_per_voxel[idx]

  return grid_candidate_center

grid_sampled_point_cloud = grid_subsampling(points, voxel_size)
grid_sample_pc_np = np.array(grid_sampled_point_cloud)


#export as STL
import matplotlib.tri as mtri

x_all = grid_sample_pc_np[:,0]
y_all = grid_sample_pc_np[:,1]
z_all = grid_sample_pc_np[:,2]

tris = mtri.Triangulation(x_all, y_all)

data = np.zeros(len(tris.triangles), dtype=mesh.Mesh.dtype)
m = mesh.Mesh(data, remove_empty_areas=False)
m.x[:] = x_all[tris.triangles]
m.y[:] = y_all[tris.triangles]
m.z[:] = z_all[tris.triangles]

m.save(args.ExportStl)

#export stl
myMesh = trimesh.load_mesh(args.ExportStl)

# scale down the mesh
scale_factor = 0.02

# Create a scale matrix
scale_matrix = trimesh.transformations.scale_matrix(scale_factor)

# Apply the scale matrix to the sphere
myMesh.apply_transform(scale_matrix)

#export obj
myMesh.export(args.ExportObj)