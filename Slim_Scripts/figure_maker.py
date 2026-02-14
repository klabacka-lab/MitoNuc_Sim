import numpy as np
from scipy import stats
import sys
import matplotlib.pyplot as plt
from pathlib import Path

def load_2d_file(path: str) -> np.ndarray:
    rows = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:          # skip blank lines
                continue
            rows.append([float(x) for x in line.split()])
    return np.array(rows, dtype=float)

arr = load_2d_file("fitness_over_time.txt")
print(arr.shape)     # (num_lines, num_values_per_line)
print(arr[0, :10])   # first 10 values of first line