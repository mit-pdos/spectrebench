#!/bin/python

import math
import subprocess
import numpy as np
import csv
from statistics import geometric_mean

subprocess.run(['g++', '-O3', '-pthread', '-o', 'lebench.bin', 'lebench.cc'])

def parse_output(stdout):
    reader = csv.reader(stdout.splitlines())
    headers = next(reader)
    times = []
    for row in reader:
        if len(row) >= 2:
            times.append(int(row[1].strip()))
        else:
            return None
    return times

means = []
for i in range(1000):
    p = subprocess.run(['./lebench.bin', '-', '10'], capture_output=True, text=True)
    times = parse_output(p.stdout)
    if times is not None:
        means.append(geometric_mean(times))
        interval = 1.96 * 100 * np.std(means) / math.sqrt(len(means)) / np.mean(means)
        print("n={}: {:.0f} ({:.0f}) ±{:.2f}%".format(len(means), np.mean(means), np.std(means), interval), flush=True)
        if i >= 10 and interval < 0.1:
            break
