import numpy as np
import os
import re

from requests import head
import json
import logging

#TODO logging + clean

def getTile(point, scale):
    moduloX = point[0]%scale
    moduloY = point[1]%scale

    tile = [point[0]-moduloX, point[1]+(scale-moduloY)]

    return tile

def getScale(file):
    file = open(file, "r")
    line_cellsize = file.readlines()[4]
    cellsize = line_cellsize.split(" ")
    scale = float(cellsize[-1:][0])

    return scale

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

def VerticalMergeAscii(tabFiles, count, outputFolder):
    files = [None] * len(tabFiles)
    for i in range (0, len(tabFiles)):
        files[i] = np.loadtxt(tabFiles[i], skiprows=6 )
    
    merged = np.vstack(files)
    
    header = writeHeader(tabFiles[0], merged)

    if not os.path.exists('merge'):
        os.makedirs('merge')
    fp=f"{outputFolder}/vmerged{count}.asc"
    np.savetxt(f"{outputFolder}/vmerged{count}.asc", merged, header=header ,fmt="%3.2f")
    return fp

def HorizontalMergeAscii(tabFiles, outputFolder):
    files = [None] * len(tabFiles)
    for i in range (0, len(tabFiles)):
        files[i] = np.loadtxt(tabFiles[i], skiprows=6 )
    
    merged = np.column_stack(files)

    header = writeHeader(tabFiles[0], merged)

    if not os.path.exists('merge'):
        os.makedirs('merge')
    fp=f"{outputFolder}/merged.asc"
    np.savetxt(f"{outputFolder}/merged.asc", merged, header=header ,fmt="%3.2f")
    return fp

def mergeASCII(InputFolder, OutputFolder, lambertData):
    #get ascii files infos
    inDir = InputFolder

    path = r"^(.*_(\d{4})_(\d{4})_.*)$"
    result= []

    for (dirpath, dirnames, filenames) in os.walk(inDir):
        print(dirpath)
        for i in range(len(filenames)):
            if filenames[i].endswith('.asc'):
                result.append(re.search(path, dirpath+"/"+filenames[i]))
    
    # get tiles
    json_object = json.loads(lambertData)

    sourcePoint = [int(json_object["latitude"]//1000),int(json_object["longitude"]//1000)]

    print(f"Point: {sourcePoint}")
    dist = 5
    scale = int(getScale(result[0].group(1)))

    logging.info(scale)

    tileCenter = getTile(sourcePoint, scale)

    pointTopLeft = [sourcePoint[0]-dist, sourcePoint[1]+dist]
    pointBottomRight = [sourcePoint[0]+dist, sourcePoint[1]-dist]

    tileTopLeft = getTile(pointTopLeft, scale)
    tileBottomRight = getTile(pointBottomRight, scale)

    tiles = []

    for x in range (tileTopLeft[0], tileBottomRight[0]+scale, scale):
        tilesSameX = []
        for y in range (tileTopLeft[1], tileBottomRight[1]-scale, -scale):
            tilesSameX.append([x, y])
        tiles.append(tilesSameX)

    print(f"TILES : {tiles}")

    fp = []
    taby = []
    for i in range(len(tiles)):
        fp.append([res.group(1) for res in result if [int(res.group(2)), int(res.group(3))] in tiles[i]])
        taby.append([res.group(3) for res in result if [int(res.group(2)), int(res.group(3))] in tiles[i]])

    fp = [f for f in fp if f != []]
    taby = [y for y in taby if y != []]

    # reverse order so the order is right for the merge
    for i in range(len(taby)):
        taby[i].sort(reverse = True)
    for i in range(len(fp)):
        fp[i].sort(reverse = True)

    print(fp)
    print(taby)

    # find max length of all tabs and fill tabs with -1 value to reach maxlength
    maxdepth=0
    for i in range (len(taby)):
        if (len(taby[i])>maxdepth):
            maxdepth = len(taby[i])

    print(f"max length : {maxdepth}")

    for i in range(len(taby)):
        if (len(taby[i]) < maxdepth) :
            taby[i].append('-1')

    max_of_rows = []
    for i in range(maxdepth):
        row = []
        for column in taby:
            row.append(column[i])
        max_of_rows.append(max(row))

    for c in range(len(taby)):
        for r in range(maxdepth):
            if (taby[c][r] < max_of_rows[r]):
                taby[c].insert(r, max_of_rows[r])
                if (int(scale) == 25):
                    fp[c].insert(r, 'external_files/ascii_nodata_25M.asc')
                if (int(scale) == 5):
                    fp[c].insert(r, 'external_files/ascii_nodata_5M.asc')
                if (int(scale) == 1):
                    fp[c].insert(r, 'external_files/ascii_nodata_1M.asc')
                
    print(fp)

    print(dirpath)

    print("vertical merge \n")
    verticalMergeTab = [None]*len(fp)
    for i in range(len(fp)):
        verticalMergeTab[i] = VerticalMergeAscii(fp[i], i, OutputFolder)

    print(verticalMergeTab)

    finalMerge = HorizontalMergeAscii(verticalMergeTab, OutputFolder)

    print(f"FINAL MERGE : {finalMerge}")