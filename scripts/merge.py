import sys
import traceback
import laspy
import os
#get arguments
import argparse
import shutil
import logging
import mergeAsciiTiles
import convertWgs84ToLambert93

#TODO logging
ap = argparse.ArgumentParser()
ap.add_argument("--folder", help="Folder", type=str)
ap.add_argument("--GPSFile", help="GPSFile", type=str)
ap.add_argument("--outputFolder", help="outputFolder", type=str)
args = ap.parse_args()

logging.basicConfig(level=logging.INFO)

def mergeLAS(InputFolder, OutputFolder):
    try:
        print('Running Merge LAS')

        #This is the las file to append to.  DO NOT STORE THIS FILE IN THE SAME DIRECTORY AS BELOW...
        out_las = os.path.join(OutputFolder, "merge.las")

        logging.info(f"Merged file: {out_las}")
        # Writing to sample.json
        open(out_las, "x")
        
        
        #this is a directory of las files
        inDir = InputFolder


        def append_to_las(in_las, out_las):
            with laspy.open(out_las, mode='a') as outlas:
                with laspy.open(in_las) as inlas:
                    for points in inlas.chunk_iterator(2_000_000):
                        outlas.append_points(points)


        for (dirpath, dirnames, filenames) in os.walk(inDir):
            count = 0
            # print(inDir)
            print(f"Dir Path : {dirpath}")
            for i in range(len(filenames)):
                print(filenames[i])
                if filenames[i].endswith('.las') and count == 0:
                    print("Copy")
                    # specify the file to be copied and the destination
                    src_file = dirpath+"/"+filenames[i]
                    print(src_file)
                    dst_file = out_las

                    # copy the file
                    shutil.copy(src_file, dst_file)
                    count+=1
                elif filenames[i].endswith('.las'):
                    print("append")
                    in_las = os.path.join(dirpath, filenames[i])
                    append_to_las(in_las, out_las)
                    count+=1  
        print('Finished without errors - merge_LAS.py')
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        print('Error in append las')
        print ("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError     Info:\n" + str(sys.exc_info()[1])) 


def main():
    print("Merge !")

    # mergeLAS(args.folder, args.outputFolder)

    for (dirpath, dirnames, filenames) in os.walk(args.folder):
        for inFile in filenames:
            if inFile.endswith('.las'):
                mergeLAS(args.folder, args.outputFolder)
                break
            elif inFile.endswith('.asc'):
                lambertData = convertWgs84ToLambert93.convertGPSDataToLambert93(args.GPSFile)

                mergeAsciiTiles.mergeASCII(args.folder, args.outputFolder, lambertData)
                break
    
    print("Merge Done")


if __name__ == "__main__":
    main()