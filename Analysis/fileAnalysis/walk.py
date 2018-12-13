# This helper script will create a list of files in the current directory and
# append one at a time to the fileAnalyze.py script argument to be processed
import sys
import os
from os import walk

mypath = sys.argv[1]
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break
print f
print dirpath
for x in f:
    command = "python fileAnalyze.py \"" + dirpath + x + "\""
    os.system(command)
