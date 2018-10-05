import sys              # https://stackoverflow.com/questions/6591931/getting-file-size-in-python
import os
from os import walk
mypath = '.'
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break
f.remove(sys.argv[0])
f.remove('fileAnalyze.py')
print f
for x in f:
    command = "python fileAnalyze.py \"" + x + "\""
    os.system(command)
