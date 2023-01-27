import argparse
import get_OSM_data
import generateNorth
import logging

ap = argparse.ArgumentParser()
ap.add_argument("--GPSFile", help="GPSFile", type=str)
ap.add_argument("--outputPath", help="output", type=str)
ap.add_argument("--outputFolder", help="outputFolder", type=str)
args = ap.parse_args()

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("North !")
    image = get_OSM_data.OSM_picture(args.GPSFile, args.outputFolder, 550)
    logging.info(f"Path of Image : {image}")

    generateNorth.generateNorth(image, args.outputFolder, args.output)

    logging.info("North generated")


if __name__ == "__main__":
    main()