from zipfile import ZipFile
import os
from os.path import basename
import sys

upload_directory = "uploads"
directory_name = str(sys.argv[1])

with ZipFile(os.path.join(upload_directory, directory_name + ".zip"), 'w') as z:
    for root, dirs, files in os.walk(directory_name):
        for file in files:
            z.write(os.path.join(root, file))
        for directory in dirs:
            z.write(os.path.join(root, directory))
