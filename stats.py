#!/bin/python3

import sys
import numpy as np
import math

values = []
for name in sys.argv[1:]:
    with open(name) as f:
        v = f.readline().split(', ')
        values.append([float(x) for x in v])


values = np.array(values).transpose()
for v in values:
    interval = 1.96 * 100 * np.std(v) / math.sqrt(len(v)) / np.mean(v)

    print("n={}: {:.3g} ({:.3g}) ±{:.2f}%".format(len(v), np.mean(v), np.std(v), interval))
