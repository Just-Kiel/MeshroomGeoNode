import re
import argparse
import json

# get arguments
ap = argparse.ArgumentParser()
ap.add_argument("weatherFile", help="weatherFile", type=str)
ap.add_argument("output", help="output", type=str)
args = ap.parse_args()

# get weather
with open(args.weatherFile, 'r') as inputfile2:
    
    # Reading from json file
    json_object = json.load(inputfile2)

weather = json_object["weather condition"]

#parse csv file
csv_path ='./lib/meshroom/nodes/scripts/hdri_list.csv'
csv = open(csv_path, "r")
csv = csv.read()

lines = [x for x in csv.split('\n')]
lines = lines[:-1]

path = r'^(\d*),(.*),(.*)$'
result = [re.search(path, line) for line in lines]
result = [x for x in result if x != None]

result = [result[i] for i in range(len(result)) if ((int)(result[i].group(1))) == weather]
print(result)

import requests
import os

URL = result[0].group(3)
filename = os.path.basename(URL)

print(filename)

response = requests.get(URL, stream=True)

if response.status_code == 200:
    with open(args.output+"/"+filename, 'wb') as out:
        out.write(response.content)
else:
    print('Request failed: %d' % response.status_code)