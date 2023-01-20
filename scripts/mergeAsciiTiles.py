import numpy as np
import os
import re

#get ascii files infos
inDir = "ASCII"

path = r"^(.*_(\d{4})_(\d{4})_.*)$"
result= []

for (dirpath, dirnames, filenames) in os.walk(inDir):
    print(dirpath)
    for i in range(len(filenames)):
        if filenames[i].endswith('.asc'):
            # print(dirpath+"/"+filenames[i])
            result.append(re.search(path, dirpath+"/"+filenames[i]))

# [print(res.group(1)) for res in result] #file path 
# [print(res.group(2)) for res in result] #x coordinates
# [print([res.group(2),res.group(3)]) for res in result] #y coordinates


def getTile(point, scale):
    moduloX = point[0]%scale
    moduloY = point[1]%scale
    # print(f"Point : {point}")
    # print(f"ModuloX : {moduloX}")
    # print(f"ModuloY : {moduloY}")

    tile = [point[0]-moduloX, point[1]+(scale-moduloY)]
    # print(f"dalle : {dalle}")
    return tile

def writeHeader(file, merged):
    file = open(file, "r")
    file = file.read()
    lines = [x for x in file.split('\n')]

    sizeCols = lines[2].split(" ")
    xllcorner = float(sizeCols[-1:][0])

    sizeCols = lines[3].split(" ")
    yllcorner = float(sizeCols[-1:][0])

    sizeCols = lines[4].split(" ")
    cellsize = float(sizeCols[-1:][0])

    header = "ncols    %s\n" % merged.shape[1]
    header += "nrows    %s\n" % merged.shape[0]
    header += "xllcorner %s\n" % xllcorner 
    header += "yllcorner %s\n" % yllcorner 
    header += "cellsize %s\n" % cellsize
    header += "NODATA_value -9999"

    return header

def VerticalMergeAscii(tabFiles, count):
    files = [None] * len(tabFiles)
    for i in range (0, len(tabFiles)):
        files[i] = np.loadtxt(tabFiles[i], skiprows=6 )
    
    merged = np.vstack(files)
    
    header = writeHeader(tabFiles[0], merged)

    fp=f"merge/vmerged{count}.asc"
    np.savetxt(f"merge/vmerged{count}.asc", merged, header=header ,fmt="%3.2f")
    return fp

def HorizontalMergeAscii(tabFiles):
    files = [None] * len(tabFiles)
    for i in range (0, len(tabFiles)):
        files[i] = np.loadtxt(tabFiles[i], skiprows=6 )
    
    merged = np.column_stack(files)

    header = writeHeader(tabFiles[0], merged)

    fp=f"merge/merged.asc"
    np.savetxt(f"merge/merged.asc", merged, header=header ,fmt="%3.2f")
    return fp


# get tiles
sourcePoint = [843, 6553]
dist = 30
asciiDir = "ASCII"
scale = 25

tileCenter = getTile(sourcePoint, scale)

pointTopLeft = [sourcePoint[0]-dist, sourcePoint[1]+dist]
pointBottomRight = [sourcePoint[0]+dist, sourcePoint[1]-dist]

tileTopLeft = getTile(pointTopLeft, scale)
tileBottomRight = getTile(pointBottomRight, scale)
# print(f"Tile center : {tileCenter}")
# print(f"Tile Top Left : {tileTopLeft}")
# print(f"Tile Bottom Right : {tileBottomRight}")

tiles = []

for x in range (tileTopLeft[0], tileBottomRight[0]+scale, scale):
    # print(x)
    tilesSameX = []
    for y in range (tileTopLeft[1], tileBottomRight[1]-scale, -scale):
        # print(y)
        tilesSameX.append([x, y])

    tiles.append(tilesSameX)

print(f"TILES : {tiles}")

fp = []
for i in range(len(tiles)):
    fp.append([res.group(1) for res in result if [int(res.group(2)), int(res.group(3))] in tiles[i]])


fp = [f for f in fp if f != []]
print(fp)

print("vertical merge \n")
verticalMergeTab = [None]*len(fp)
for i in range(len(fp)):
    verticalMergeTab[i] = VerticalMergeAscii(fp[i], i)

print(verticalMergeTab)

finalMerge = HorizontalMergeAscii(verticalMergeTab)

print(f"FINAL MERGE : {finalMerge}")