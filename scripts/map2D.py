import argparse
import get_OSM_data
import generatePlane

#TODO args better
ap = argparse.ArgumentParser()
ap.add_argument("GPSFile", help="GPSFile", type=str)
ap.add_argument("dist", help="dist", type=str)
ap.add_argument("output", help="output", type=str)
ap.add_argument("outputFolder", help="outputFolder", type=str)
args = ap.parse_args()


def main():
    print("2D Map !")
    image = get_OSM_data.OSM_picture(args.GPSFile, args.outputFolder, args.dist)
    print(f"Path of Image : {image}")

    generatePlane.generatePlane(image, args.outputFolder, args.output)

    print("2D Map generated")


if __name__ == "__main__":
    main()