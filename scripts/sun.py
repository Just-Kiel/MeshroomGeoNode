import getTimeDataset
import sunPosition
import argparse
import generateSun

ap = argparse.ArgumentParser()
ap.add_argument("--inputFile", help="input SFM data", type=str)
ap.add_argument("--GPSFile", help="GPS file", type=str)
ap.add_argument("--outputPath", help="output path", type=str)
ap.add_argument("--outputFolder", help="output folder", type=str)
args = ap.parse_args()


def main():
    print("Sun!")
    time = getTimeDataset.timeOfDataset(args.inputFile, args.GPSFile)
    print(f"Time of Dataset : {time}")

    sunPos = sunPosition.getSunPosition3DEnv(args.GPSFile, time)
    print(f"Sun position : {sunPos}")

    generateSun.generateSun(args.outputFolder, sunPos)

    print("Sun generated")


if __name__ == "__main__":
    main()