import argparse
import get_OSM_data
import generatePlane
import logging

ap = argparse.ArgumentParser()
ap.add_argument("--GPSFile", help="GPSFile", type=str)
ap.add_argument("--dist", help="dist", type=str)
ap.add_argument("--outputPath", help="output", type=str)
ap.add_argument("--outputFolder", help="outputFolder", type=str)
args = ap.parse_args()

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("2D Map !")
    image = get_OSM_data.OSM_picture(args.GPSFile, args.outputFolder, args.dist)
    logging.info(f"Path of Image : {image}")

    generatePlane.generatePlane(image, args.outputFolder, args.outputPath)

    logging.info("2D Map generated")


if __name__ == "__main__":
    main()