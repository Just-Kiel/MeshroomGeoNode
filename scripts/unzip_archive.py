# import py7zr
import glob
import os
import sys

argv = sys.argv
argv = [element if "--" not in element else "" for element in argv]
argv = [x for x in argv if x != ""]

archive_to_unzip = argv[1]
output_folder = argv[4]

dir_unzip = archive_to_unzip.replace('/', '\\')

dir_unzip=glob.glob(dir_unzip+"/*.7z")[0]

from py7zr import unpack_7zarchive
import shutil

shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
shutil.unpack_archive(dir_unzip, output_folder)

# for fname in os.listdir(output_folder):
#     if fname.isdir:
#         dl_wait = False
#         old_name = fname
#         os.rename(dir_output+r'/'+old_name, dir_output+r'/lidar.7z')

with os.scandir(output_folder) as itr:
    for entry in itr:
        if entry.is_dir():
            old_name = entry.name
            os.rename(output_folder+r'/'+old_name, output_folder+'/unzip')

# os.rename(output_folder, output_folder)