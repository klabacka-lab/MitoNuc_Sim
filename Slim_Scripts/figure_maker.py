import numpy as np
from scipy import stats
import sys
import matplotlib.pyplot as plt
from pathlib import Path

BOXPLOT = True
LOG_SCALE = False
MEASURE_FITNESS_GAP = False

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

sexual_std_dev = sexual_arr.std(axis=0)
asexual_arr = asexual_arr.std(axis=0)

sexual_arr = sexual_arr.mean(axis=0)
asexual_arr = asexual_arr.mean(axis=0)

if MEASURE_FITNESS_GAP:
    sexual_arr = 1- sexual_arr
    asexual_arr = 1- asexual_arr

cycles = np.array(range(1, sexual_arr.shape[0] + 1))


#Load final fitness data
sexual_final_fitness = np.loadtxt("sexual_final_fitness.txt")
asexual_final_fitness = np.loadtxt("asexual_final_fitness.txt")

fig, axes = plt.subplots(1, 2, figsize=(12,5))

# ----- Left: Mean fitness over time
axes[0].scatter(cycles, asexual_arr, label="Asexual", color="blue")
axes[0].scatter(cycles, sexual_arr, label="Sexual", color="orange")

axes[0].set_xlabel("Cycle")
axes[0].set_ylabel("Mean Fitness")
if LOG_SCALE:
    axes[0].set_yscale('log')      # Logarithmic y-axis
axes[0].set_title("Mean Fitness Over Time")
axes[0].legend()
axes[0].grid(True)

# ----- Right: Final fitness distribution (boxplots)
if BOXPLOT:
    bp = axes[1].boxplot(
        [asexual_final_fitness, sexual_final_fitness],
        tick_labels=["Asexual", "Sexual"],
        patch_artist=True  # <-- allows filling colors
    )

    colors = ["blue", "orange"]

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    for median in bp["medians"]:
        median.set_color("black")
        median.set_linewidth(2)

else:
    axes[1].hist(asexual_final_fitness, bins=15, alpha=0.6, label="Asexual", color="blue")
    axes[1].hist(sexual_final_fitness, bins=15, alpha=0.6, label="Sexual", color="orange")

axes[1].set_xlabel("Final Fitness")
axes[1].set_ylabel("Frequency")
axes[1].set_title("Final Fitness Distribution")
#axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("fitness_over_time.png", dpi=300)