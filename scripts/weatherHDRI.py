import argparse
import getTimeDataset
import get_weather
import get_hdri

#TODO logging + better args
ap = argparse.ArgumentParser()
ap.add_argument("inputFile", help="input SFM data", type=str)
ap.add_argument("GPSFile", help="GPSFile", type=str)
ap.add_argument("output", help="output", type=str)
args = ap.parse_args()

def main():
    print("Weather !")
    time = getTimeDataset.timeOfDataset(args.inputFile, args.GPSFile)
    print(f"Time of Dataset : {time}")

    weather = get_weather.getWeather(args.GPSFile, time)
    print(f"Weather : {weather}")

    get_hdri.getHDRI(weather, args.output)

    print("Weather HDRI generated")

if __name__ == "__main__":
    main()