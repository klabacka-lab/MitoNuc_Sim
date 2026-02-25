import string

import numpy as np
from scipy import stats
import sys
import matplotlib.pyplot as plt
from pathlib import Path

BOXPLOT = True
LOG_SCALE = False
MEASURE_FITNESS_GAP = False
SCATTER = False
FIT_LINE = False

def load_2d_array(path: str) -> np.ndarray:
    rows = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:          # skip blank lines
                continue
            rows.append([float(x) for x in line.split()])
    return np.array(rows, dtype=float)

sexual_mean = load_2d_array("sexual_fitness_over_time.txt")
asexual_mean = load_2d_array("asexual_fitness_over_time.txt")

sexual_std_dev = sexual_mean.std(axis=0)
asexual_std_dev = asexual_mean.std(axis=0)

sexual_mean = sexual_mean.mean(axis=0)
asexual_mean = asexual_mean.mean(axis=0)



if MEASURE_FITNESS_GAP:
    sexual_mean = 1- sexual_mean
    asexual_mean = 1- asexual_mean

cycles = np.array(range(1, sexual_mean.shape[0] + 1))

if FIT_LINE:
    from scipy.optimize import curve_fit

    # Define asymptotic function
    def model_function(x, a, b, c):
        return a - b * np.exp(-c * x)

    # Fit curve
    popt, pcov = curve_fit(model_function, cycles, sexual_mean, p0 = [1.0, 0.1, 0.001])
    #print the lie of best fit as string 
    print(f"Line of best fit for sexual: y = {popt[0]:.4f} - {popt[1]:.4f} * exp(-{popt[2]:.4f} * x)")

    # Fit curve
    popt, pcov = curve_fit(model_function, cycles, asexual_mean, p0 = [1.0, 0.1, 0.001])
    #print the lie of best fit as string 
    print(f"Line of best fit for asexual: y = {popt[0]:.4f} - {popt[1]:.4f} * exp(-{popt[2]:.4f} * x)")


#Load final fitness data
sexual_final_fitness = np.loadtxt("sexual_final_fitness.txt")
asexual_final_fitness = np.loadtxt("asexual_final_fitness.txt")

fig, axes = plt.subplots(1, 2, figsize=(12,5), sharey=True)

# ----- Left: Mean fitness over time
if SCATTER:
    axes[0].scatter(cycles, asexual_mean, label="Asexual", color="blue", s = 1)
    axes[0].scatter(cycles, sexual_mean, label="Sexual", color="orange", s = 1)
else:
    axes[0].plot(cycles, asexual_mean, color="blue", label="Asexual Mean")
    axes[0].fill_between(cycles, asexual_mean - asexual_std_dev, asexual_mean + asexual_std_dev, alpha=0.3, color="blue", label="Asexual ±1 SD")
    axes[0].plot(cycles, sexual_mean, color="orange", label="Sexual Mean")
    axes[0].fill_between(cycles, sexual_mean - sexual_std_dev, sexual_mean + sexual_std_dev, alpha=0.3, color="orange", label="Sexual ±1 SD")


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

axes[1].set_title("Final Fitness Distribution")
#axes[1].legend()
axes[1].grid(True, alpha=0.3)

for ax, label in zip(axes.flat, string.ascii_uppercase):
    ax.text(0.02, 0.98, f"({label})",
            transform=ax.transAxes,
            fontsize=14,
            fontweight='bold',
            va='top')

plt.tight_layout()
plt.savefig("fitness_over_time.png", dpi=300)
