import re
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("DepartmentFile", help="DepartmentFile", type=str)
ap.add_argument("Scan3dType", help="Scan3dType", type=str)
ap.add_argument("output", help="outputValue", type=str)
args = ap.parse_args()

with open(args.DepartmentFile, 'r') as inputfile:
    # Reading from json file
    json_object = json.load(inputfile)

postcode = json_object["postcode"]
dp_name = json_object["region"]

csv_path ='./lib/meshroom/nodes/scripts/RGE_Alti_1m.csv' #default
if args.Scan3dType == '5m': csv_path = './lib/meshroom/nodes/scripts/RGE_Alti_5m.csv'
if args.Scan3dType == '25m': csv_path = './lib/meshroom/nodes/scripts/BD_Alti_25m.csv'
csv = open(csv_path, "r")
csv = csv.read()

lines = [x for x in csv.split('\n')]
lines = lines[:-1]

path = r'^(\d{1}\w{0,3}),(.*[a-zA-Z]),(?:"?)(.*\w)(?:"?)$'
result = [re.search(path, line) for line in lines]
result = [x for x in result if x != None]

result = [result[i] for i in range(len(result)) if (result[i].group(2)) == dp_name]

# 1. On importe la bibliothèque requests
import requests
import os

for i in range(len(result)):
    links = result[i].group(3).split(',')
    for j in range (len(links)):
        filename = os.path.basename(links[j])
        print(filename)
        response = requests.get(links[j], stream=True)

        if response.status_code == 200:
            with open(args.output+"/"+filename, 'wb') as out:
                out.write(response.content)
        else:
            print('Request failed: %d' % response.status_code)
