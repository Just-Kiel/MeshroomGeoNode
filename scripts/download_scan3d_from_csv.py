import re

import logging
import requests
import os
from unidecode import unidecode
import shutil

#TODO clean
def download(departementData: dict, Resolution, OutputFolder):
    # log some messages
    logging.info('This is an info message.')

    postcode = departementData["postcode"]
    dp_name = departementData["region"]

    logging.info(f"Resolution: {int(Resolution)}")

    if int(Resolution) == 1: csv_path ='./lib/meshroom/nodes/external_files/RGE_Alti_1m.csv' #default
    if int(Resolution) == 5: csv_path = './lib/meshroom/nodes/external_files/RGE_Alti_5m.csv'
    if int(Resolution) == 25: csv_path = './lib/meshroom/nodes/external_files/BD_Alti_25m.csv'

    logging.info(f"Path : {csv_path}")
    csv = open(csv_path, "r")
    csv = csv.read()

    lines = [x for x in csv.split('\n')]
    lines = lines[:-1]

    path = r'^(\d{1,}(?:[A-Z]?)),(.*[a-zA-Z]),(?:"?)(.*\w).*$'
    result = [re.search(path, line) for line in lines]
    result = [x for x in result if x != None]

    names = [re.sub('[^0-9a-zA-Z]+', ' ', str(result[i].group(2))) for i in range(len(result))]
    dp_name = re.sub('[^0-9a-zA-Z]+', ' ', dp_name)

    result = [result[i] for i in range(len(result)) if (result[i].group(1)) == dp_name]

    # result = [r for r in result if (r.group(1)) == dp_name]

    logging.info(result)

    for i in range(len(result)):
        links = result[i].group(3).split(',')
        for j in range (len(links)):
            filename = os.path.basename(links[j])
            logging.info(filename)
            response = requests.get(links[j], stream=True)

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
                logging.info('Request failed: %d' % response.status_code)
    
    return OutputFolder+"/"+filename

def extractFromFolder(UnzipPath, OutputFolder):
    for (dirpath, dirnames, filenames) in os.walk(UnzipPath):
        # print(dirpath)
        for inFile in filenames:
            if inFile.endswith('.asc'):	
                shutil.move(dirpath + "/" + inFile, OutputFolder+ "/"+ inFile)

#TODO replace + "/" + with os.path.join(dirpath, inFile)
#TODO logging instead of logger
#TODO requirements.txt
#TODO relocate ASCII
#TODO OSM layers