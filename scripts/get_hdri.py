import re
import argparse
import json

import logging

# create a logger with a specified name
logger = logging.getLogger('logger_hdri')

# set the logging level
logger.setLevel(logging.DEBUG)

# create a file handler to write logs to a file
file_handler = logging.FileHandler('logger_hdri.log')

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

import requests
import os

URL = result[0].group(3)
filename = os.path.basename(URL)

response = requests.get(URL, stream=True)

if response.status_code == 200:
    logger.info("Download started")

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    # write the data to a file
    with open(args.output, 'wb') as out:
        for data in response.iter_content(block_size):
            wrote = wrote + len(data)
            progress = wrote / total_size * 100
            logger.info(f'Download Progress: {progress}%')
            out.write(data)
else:
    print('Request failed: %d' % response.status_code)