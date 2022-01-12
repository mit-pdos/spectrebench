#!/bin/python3

import sys
import numpy as np

values = []
for name in sys.argv[1:]:
    with open(name) as f:
        v = f.readline().split(', ')
        values.append([float(x) for x in v])


values = np.array(values).transpose()
for v in values:
    print("{} ({})".format(np.mean(v), np.std(v)))
