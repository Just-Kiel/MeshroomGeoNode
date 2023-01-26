import re
import json

import logging
import requests
import os

#TODO logging + clean
def download(Lambert93Data, OutputFolder):
    # log some messages
    logging.info('This is an info message.')

    # Reading from json file
    json_object = json.loads(Lambert93Data)

    x = json_object["latitude"]
    y = json_object["longitude"]

    x=(x/1000) #meters to km
    y=(y/1000)
    # for x
    x = int(x) if int(x)%2==0 else int(x)-1
    # for y
    y = int(y)+2 if int(y)%2!=0 else int(y)+1

    path = r"^.*-(\d{4,})_(\d{4,})-\d{4,},(.*).*$"
    fichier = open("./lib/meshroom/nodes/external_files/TA_diff_pkk_lidarhd.csv", "r")
    fichier = fichier.read()

    lines = [x for x in fichier.split('\n')]
    lines = lines[:-1]


    result = [re.search(path, line) for line in lines]
    result = [x for x in result if x != None]

    result = [result[i] for i in range(len(result)) if int(result[i].group(1)) == x and int(result[i].group(2)) == y]

    URL = result[0].group(3)
    filename = os.path.basename(URL)

    logging.info(filename)

    response = requests.get(URL, stream=True)

    if response.status_code == 200:
        logging.info("Download started")

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0
        # write the data to a file
        with open(OutputFolder+"/"+filename, "wb") as f:
            for data in response.iter_content(block_size):
                wrote = wrote + len(data)
                progress = wrote / total_size * 100
                logging.info(f'Download Progress: {progress}%')
                f.write(data)
    else:
        print('Request failed: %d' % response.status_code)

    return OutputFolder+"/"+filename

    