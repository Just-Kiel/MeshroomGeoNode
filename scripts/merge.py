import sys
import traceback
import laspy
import os
#get arguments
import argparse
import shutil

ap = argparse.ArgumentParser()
ap.add_argument("LAStoMerge", help="LAStoMerge", type=str)
ap.add_argument("output", help="output", type=str)
args = ap.parse_args()

try:
    print('Running Merge LAS')

    #This is the las file to append to.  DO NOT STORE THIS FILE IN THE SAME DIRECTORY AS BELOW...
    out_las = args.output

    # Writing to sample.json
    open(out_las, "x")
    
    #this is a directory of las files
    inDir = args.LAStoMerge


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