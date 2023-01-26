import re
import json

import logging
import requests


def getHDRI(WeatherData, output):
    # log some messages
    logging.info('This is an info message.')

    # get weather     
    # Reading from json file
    json_object = json.loads(WeatherData)

    weather = json_object["weather condition"]

    #parse csv file
    csv_path ='./lib/meshroom/nodes/external_files/hdri_list.csv'
    csv = open(csv_path, "r")
    csv = csv.read()

    lines = [x for x in csv.split('\n')]
    lines = lines[:-1]

    path = r'^(\d*),(.*),(.*)$'
    result = [re.search(path, line) for line in lines]
    result = [x for x in result if x != None]

    result = [result[i] for i in range(len(result)) if ((int)(result[i].group(1))) == weather]

    URL = result[0].group(3)
    response = requests.get(URL, stream=True)

    if response.status_code == 200:
        logging.info("Download started")

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0
        # write the data to a file
        with open(output, 'wb') as out:
            for data in response.iter_content(block_size):
                wrote = wrote + len(data)
                progress = wrote / total_size * 100
                logging.info(f'Download Progress: {progress}%')
                out.write(data)
    else:
        logging.info('Request failed: %d' % response.status_code)