# This script checks a file with a list of types and returned only the unique types
# Run FileAnalyze.py with only attribList[4] printed to text file to get a list of file types.
inputFile = 'fileTypes.txt'

from collections import Counter, OrderedDict
class OrderedCounter(Counter, OrderedDict):
    pass

with open(inputFile) as f:
    seen = OrderedCounter([line.strip() for line in f])
    print("\n".join([k for k,v in seen.items() if v == 1]))
