import argparse
import os
import convertWgs84ToLambert93
import Ascii_Lidar_To_Mesh
import logging

ap = argparse.ArgumentParser()
ap.add_argument("--folder", help="input folder", type=str)
ap.add_argument("--GPSFile", help="input folder", type=str)
ap.add_argument("--MeshMethod", help="mesh method", type=str)
ap.add_argument("--dist", help="distance", type=str)
ap.add_argument("--outputobj", help="outputobj", type=str)
args = ap.parse_args()

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Mesh 3D !")

    lambertData = convertWgs84ToLambert93.convertGPSDataToLambert93(args.GPSFile)

    logging.info(f"Mesh method: {args.MeshMethod}")

    for (dirpath, dirnames, filenames) in os.walk(args.folder):
        for inFile in filenames:
            if inFile.endswith('.las') or inFile.endswith('.asc'):
                Ascii_Lidar_To_Mesh.meshing(os.path.join(dirpath +"/"+inFile), int(args.dist), args.MeshMethod, lambertData, args.outputobj)
                break
    
    logging.info("Mesh 3D Done")


if __name__ == "__main__":
    main()