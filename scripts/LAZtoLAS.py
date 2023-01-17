import sys
import traceback
#import pylas
import laspy
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("LAZFolder", help="LAZFolder", type=str)
ap.add_argument("exportFolderName", help="exportFolderName", type=str)
args = ap.parse_args()

try:
    print('Running LAZ_to_LAS.py')
    
    def convert_laz_to_las(in_laz, out_las):
        las = laspy.read(in_laz)
        las = laspy.convert(las)
        las.write(out_las)        
    
    in_dir = args.LAZFolder
    
    for (dirpath, dirnames, filenames) in os.walk(in_dir):
        for inFile in filenames:
            if inFile.endswith('.laz'):	
                in_laz = os.path.join(dirpath,inFile)
                
                out_las = args.exportFolderName+"/"+inFile
                out_las = out_las.replace('laz', 'las') 
                print('working on file: ',out_las)
                convert_laz_to_las(in_laz, out_las)
                             
    print('Finished without errors - LAZ_to_LAS.py')
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    print('Error in read_xmp.py')
    print ("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1]))    