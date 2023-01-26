import argparse
import get_OSM_data
import generateNorth

#TODO args better
ap = argparse.ArgumentParser()
ap.add_argument("GPSFile", help="GPSFile", type=str)
ap.add_argument("output", help="output", type=str)
ap.add_argument("outputFolder", help="outputFolder", type=str)
args = ap.parse_args()


def main():
    print("North !")
    image = get_OSM_data.OSM_picture(args.GPSFile, args.outputFolder, 550)
    print(f"Path of Image : {image}")

    generateNorth.generateNorth(image, args.outputFolder, args.output)

    print("North generated")


if __name__ == "__main__":
    main()