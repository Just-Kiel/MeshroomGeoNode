import re
import glob
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("Lambert93File", help="Lambert93File", type=str)
ap.add_argument("output", help="outputValue", type=str)
args = ap.parse_args()

with open(args.Lambert93File, 'r') as inputfile:
    # Reading from json file
    json_object = json.load(inputfile)

x = json_object["latitude"]
y = json_object["longitude"]

x=(x/1000) #meters to km
y=(y/1000)
# for x
x = int(x) if int(x)%2==0 else int(x)-1
# for y TODO because wrong
y = int(y)+2 if int(y)%2!=0 else int(y)+1

#887
# if int(887)%2==0 int(887)
# else int(887)-1
#6245, 3545616516
#6244
# if (int(6245)%2 !=0) int(6245)+= 2
# else int(6244)+=1

print(y)

path = r"^.*-(\d{4,})_(\d{4,})-\d{4,},(.*).*$"
fichier = open("./lib/meshroom/nodes/scripts/TA_diff_pkk_lidarhd.csv", "r")
fichier = fichier.read()

lines = [x for x in fichier.split('\n')]
lines = lines[:-1]


result = [re.search(path, line) for line in lines]
result = [x for x in result if x != None]

result = [result[i] for i in range(len(result)) if int(result[i].group(1)) == x and int(result[i].group(2)) == y]


# 1. On importe la bibliothèque requests
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

# print(glob.glob("./lib/meshroom/nodes/scripts/*.7z"))