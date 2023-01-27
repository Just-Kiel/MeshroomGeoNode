import argparse
import getTimeDataset
import get_weather
import get_hdri
import logging

ap = argparse.ArgumentParser()
ap.add_argument("--inputFile", help="input SFM data", type=str)
ap.add_argument("--GPSFile", help="GPSFile", type=str)
ap.add_argument("--output", help="output", type=str)
args = ap.parse_args()

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Weather !")
    time = getTimeDataset.timeOfDataset(args.inputFile, args.GPSFile)
    logging.info(f"Time of Dataset : {time}")

    weather = get_weather.getWeather(args.GPSFile, time)
    logging.info(f"Weather : {weather}")

    get_hdri.getHDRI(weather, args.output)

    logging.info("Weather HDRI generated")

if __name__ == "__main__":
    main()