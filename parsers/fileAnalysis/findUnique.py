from collections import Counter, OrderedDict

class OrderedCounter(Counter, OrderedDict):
    pass

with open('fileTypes.txt') as f:
    seen = OrderedCounter([line.strip() for line in f])
    print("\n".join([k for k,v in seen.items() if v == 1]))