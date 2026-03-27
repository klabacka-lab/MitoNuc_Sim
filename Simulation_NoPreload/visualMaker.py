import string
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# -----------------------------
# Configuration Flags
# -----------------------------

sexual = sys.argv[1]
asexual = sys.argv[2]



File1Name = sexual.split("/")[-1].rstrip(".csv")
File2Name = asexual.split("/")[-1].rstrip(".csv")
Filepath = sexual.split("/")[0]
output = f"./NoPreload_Figures/{File1Name}_X_{File2Name}.png"

BOXPLOT = True
LOG_SCALE = False
MEASURE_FITNESS_GAP = False
SCATTER = False

SEXUAL_COLOR = "orange"
ASEXUAL_COLOR = "blue"

# -----------------------------
# Filename Parser
# -----------------------------

def parse_filename_label(path: str) -> str:
    name = Path(path).stem
    parts = name.split("_")

    reproduction = "Unknown"
    epistasis = ""
    params = []

    if "sex" in parts:
        reproduction = "Sexual"
    elif "asex" in parts:
        reproduction = "Asexual"

    if "epi" in parts:
        epistasis = "Epi"
    elif "noepi" in parts:
        epistasis = "No Epi"

    for p in parts:
        try:
            float(p)
            params.append(p)
        except ValueError:
            continue

    param_str = ", ".join(params)

    return f"{reproduction} ({epistasis}) [{param_str}]"

# -----------------------------
# Safe Loaders
# -----------------------------

def compute_stats(arr: np.ndarray):
    if arr.size == 0:
        return np.array([]), np.array([])

    if arr.ndim == 1:
        return arr, np.zeros_like(arr)
    
    return arr.mean(axis=0), arr.std(axis=0)

# -----------------------------
# Load Data
# -----------------------------

sexual_data = np.loadtxt(sexual, delimiter=",")
asexual_data = np.loadtxt(asexual, delimiter=",")

# Ensure 2D
sexual_data = np.atleast_2d(sexual_data)
asexual_data = np.atleast_2d(asexual_data)

print(f"Sexual shape: {sexual_data.shape}")
print(f"Asexual shape: {asexual_data.shape}")

# Labels from filenames
sexual_label = parse_filename_label(sexual)
asexual_label = parse_filename_label(asexual)

# -----------------------------
# Compute Statistics
# -----------------------------

sexual_mean, sexual_std_dev = compute_stats(sexual_data)
asexual_mean, asexual_std_dev = compute_stats(asexual_data)

sexual_n = sexual_data.shape[0]
asexual_n = asexual_data.shape[0]

sexual_ci = np.zeros_like(sexual_mean)
asexual_ci = np.zeros_like(asexual_mean)

if sexual_n > 0:
    sexual_ci = 1.96 * sexual_std_dev / np.sqrt(sexual_n)

if asexual_n > 0:
    asexual_ci = 1.96 * asexual_std_dev / np.sqrt(asexual_n)

if MEASURE_FITNESS_GAP:
    sexual_mean = 1 - sexual_mean
    asexual_mean = 1 - asexual_mean

# -----------------------------
# Final Generation Fitness
# -----------------------------

sexual_final_fitness = sexual_data[:, -1]
asexual_final_fitness = asexual_data[:, -1]

# -----------------------------
# Plotting
# -----------------------------

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ---- Left Panel: Time-Series

any_time_series = False

if asexual_mean.size > 0:
    x = np.arange(1, len(asexual_mean) + 1)
    if SCATTER:
        axes[0].scatter(x, asexual_mean, s=4, color=ASEXUAL_COLOR,
                        label=asexual_label)
    else:
        axes[0].plot(x, asexual_mean, color=ASEXUAL_COLOR,
                     label=f"{asexual_label} Mean")
        axes[0].fill_between(
            x,
            asexual_mean - asexual_std_dev,
            asexual_mean + asexual_std_dev,
            alpha=0.3,
            color=ASEXUAL_COLOR
        )
    any_time_series = True

if sexual_mean.size > 0:
    x = np.arange(1, len(sexual_mean) + 1)
    if SCATTER:
        axes[0].scatter(x, sexual_mean, s=4, color=SEXUAL_COLOR,
                        label=sexual_label)
    else:
        axes[0].plot(x, sexual_mean, color=SEXUAL_COLOR,
                     label=f"{sexual_label} Mean")
        axes[0].fill_between(
            x,
            sexual_mean - sexual_std_dev,
            sexual_mean + sexual_std_dev,
            alpha=0.3,
            color=SEXUAL_COLOR
        )
    any_time_series = True

if not any_time_series:
    axes[0].text(0.5, 0.5, "No time-series data",
                 transform=axes[0].transAxes,
                 ha="center", va="center")

axes[0].set_xlabel("Generation")
axes[0].set_ylabel("Mean Fitness")

if sexual_n == asexual_n and sexual_n > 0:
    axes[0].set_title(f"Mean Fitness Over Time ({sexual_n} Simulations)")
else:
    axes[0].set_title(
        f"Mean Fitness Over Time "
        f"(Sexual: {sexual_n}, Asexual: {asexual_n})"
    )

axes[0].grid(True)

if LOG_SCALE:
    axes[0].set_yscale('log')

if axes[0].get_legend_handles_labels()[0]:
    axes[0].legend()

# ---- Right Panel: Final Fitness Distribution

box_data = []
tick_labels = []

box_data.append(asexual_final_fitness if asexual_final_fitness.size > 0 else [])
tick_labels.append(asexual_label)

box_data.append(sexual_final_fitness if sexual_final_fitness.size > 0 else [])
tick_labels.append(sexual_label)

if BOXPLOT:
    bp = axes[1].boxplot(
        box_data,
        patch_artist=True,
        tick_labels=tick_labels
    )

    colors = [ASEXUAL_COLOR, SEXUAL_COLOR]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    for median in bp["medians"]:
        median.set_color("black")
        median.set_linewidth(2)

else:
    if asexual_final_fitness.size > 0:
        axes[1].hist(asexual_final_fitness, bins=15,
                     alpha=0.6, color=ASEXUAL_COLOR,
                     label=asexual_label)

    if sexual_final_fitness.size > 0:
        axes[1].hist(sexual_final_fitness, bins=15,
                     alpha=0.6, color=SEXUAL_COLOR,
                     label=sexual_label)

axes[1].set_title("Fitness Distribution After Final Generation")
axes[1].set_xlabel("Reproduction Method")
axes[1].grid(True, alpha=0.3)

if axes[1].get_legend_handles_labels()[0]:
    axes[1].legend()

# ---- Panel Labels

for ax, label in zip(axes.flat, string.ascii_uppercase):
    ax.text(0.02, 0.98, f"({label})",
            transform=ax.transAxes,
            fontsize=14,
            fontweight='bold',
            va='top')

plt.tight_layout()
plt.savefig(output, dpi=300)
print(f"Saved: {output}")