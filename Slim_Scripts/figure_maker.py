import numpy as np
from scipy import stats
import sys
import matplotlib.pyplot as plt
from pathlib import Path

def load_2d_array(path: str) -> np.ndarray:
    rows = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:          # skip blank lines
                continue
            rows.append([float(x) for x in line.split()])
    return np.array(rows, dtype=float)

sexual_arr = load_2d_array("sexual_fitness_over_time.txt")
asexual_arr = load_2d_array("asexual_fitness_over_time.txt")

sexual_arr = sexual_arr.mean(axis=0)
asexual_arr = asexual_arr.mean(axis=0)

print(sexual_arr.shape)
print(asexual_arr.shape)
cycles = np.array(range(1, sexual_arr.shape[0] + 1))


#Load final fitness data
sexual_final_fitness = np.loadtxt("sexual_final_fitness.txt")
asexual_final_fitness = np.loadtxt("asexual_final_fitness.txt")

fig, axes = plt.subplots(1, 2, figsize=(12,5))

# ----- Left: Mean fitness over time
axes[0].plot(cycles, asexual_arr, label="Asexual", color="blue")
axes[0].plot(cycles, sexual_arr, label="Sexual", color="orange")

axes[0].set_xlabel("Cycle")
axes[0].set_ylabel("Mean Fitness")
axes[0].set_title("Mean Fitness Over Time")
axes[0].legend()
axes[0].grid(True)

# ----- Right: Final fitness distribution (boxplots)
axes[1].hist(asexual_final_fitness, bins=15, alpha=0.6, label="Asexual", color="blue")
axes[1].hist(sexual_final_fitness, bins=15, alpha=0.6, label="Sexual", color="orange")

axes[1].set_xlabel("Final Fitness")
axes[1].set_ylabel("Frequency")
axes[1].set_title("Final Fitness Distribution")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("fitness_over_time.png", dpi=300)
plt.show()