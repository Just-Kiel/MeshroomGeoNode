import re
import argparse
import json

import logging

# create a logger with a specified name
logger = logging.getLogger('mylogger')

# set the logging level
logger.setLevel(logging.DEBUG)

# create a file handler to write logs to a file
file_handler = logging.FileHandler('mylog.log')

# create a stream handler to write logs to the console
stream_handler = logging.StreamHandler()

# set the logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# log some messages
logger.info('This is an info message.')


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

if args.Scan3dType == '1m': csv_path ='./lib/meshroom/nodes/scripts/RGE_Alti_1m.csv' #default
if args.Scan3dType == '5m': csv_path = './lib/meshroom/nodes/scripts/RGE_Alti_5m.csv'
if args.Scan3dType == '25m': csv_path = './lib/meshroom/nodes/scripts/BD_Alti_25m.csv'
csv = open(csv_path, "r")
csv = csv.read()

lines = [x for x in csv.split('\n')]
lines = lines[:-1]

path = r'^(\d{1,}(?:[A-Z]?)),(.*[a-zA-Z]),(?:"?)(.*\w).*$'
result = [re.search(path, line) for line in lines]
result = [x for x in result if x != None]

result = [result[i] for i in range(len(result)) if (result[i].group(2)) == dp_name]

# 1. On importe la bibliothèque requests
import requests
import os

print(result)

for i in range(len(result)):
    links = result[i].group(3).split(',')
    for j in range (len(links)):
        filename = os.path.basename(links[j])
        print(filename)
        response = requests.get(links[j], stream=True)

        if response.status_code == 200:
            logger.info("Download started")

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            wrote = 0
            # write the data to a file
            with open(args.output+"/"+filename, "wb") as f:
                for data in response.iter_content(block_size):
                    wrote = wrote + len(data)
                    progress = wrote / total_size * 100
                    logger.info(f'Download Progress: {progress}%')
                    f.write(data)
        else:
            print('Request failed: %d' % response.status_code)
