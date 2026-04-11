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
output = f"./NoPreload_Figures/{File1Name}_X_{File2Name}.png"

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
# Stats: Median and IQR
# -----------------------------

def compute_stats(arr: np.ndarray):
    if arr.size == 0:
        return np.array([]), np.array([]), np.array([])

    if arr.ndim == 1:
        return arr, arr, arr

    median = np.median(arr, axis=0)
    q1 = np.percentile(arr, 25, axis=0)
    q3 = np.percentile(arr, 75, axis=0)

    return median, q1, q3

# -----------------------------
# Load Data
# -----------------------------

sexual_data = np.loadtxt(sexual, delimiter=",")
asexual_data = np.loadtxt(asexual, delimiter=",")

sexual_data = np.atleast_2d(sexual_data)
asexual_data = np.atleast_2d(asexual_data)

print(f"Sexual shape: {sexual_data.shape}")
print(f"Asexual shape: {asexual_data.shape}")

sexual_label = parse_filename_label(sexual)
asexual_label = parse_filename_label(asexual)

# -----------------------------
# Compute Statistics
# -----------------------------

sexual_median, sexual_q1, sexual_q3 = compute_stats(sexual_data)
asexual_median, asexual_q1, asexual_q3 = compute_stats(asexual_data)

sexual_n = sexual_data.shape[0]
asexual_n = asexual_data.shape[0]

if MEASURE_FITNESS_GAP:
    sexual_median = 1 - sexual_median
    asexual_median = 1 - asexual_median
    sexual_q1 = 1 - sexual_q1
    sexual_q3 = 1 - sexual_q3
    asexual_q1 = 1 - asexual_q1
    asexual_q3 = 1 - asexual_q3

# -----------------------------
# Plotting
# -----------------------------

fig, ax = plt.subplots(figsize=(7, 5))

any_time_series = False

# Asexual
if asexual_median.size > 0:
    x = np.arange(1, len(asexual_median) + 1)
    if SCATTER:
        ax.scatter(x, asexual_median, s=4,
                   color=ASEXUAL_COLOR, label=asexual_label)
    else:
        ax.plot(x, asexual_median,
                color=ASEXUAL_COLOR,
                label=f"{asexual_label} Median")
        ax.fill_between(
            x,
            asexual_q1,
            asexual_q3,
            alpha=0.3,
            color=ASEXUAL_COLOR
        )
    any_time_series = True

# Sexual
if sexual_median.size > 0:
    x = np.arange(1, len(sexual_median) + 1)
    if SCATTER:
        ax.scatter(x, sexual_median, s=4,
                   color=SEXUAL_COLOR, label=sexual_label)
    else:
        ax.plot(x, sexual_median,
                color=SEXUAL_COLOR,
                label=f"{sexual_label} Median")
        ax.fill_between(
            x,
            sexual_q1,
            sexual_q3,
            alpha=0.3,
            color=SEXUAL_COLOR
        )
    any_time_series = True

if not any_time_series:
    ax.text(0.5, 0.5, "No data",
            transform=ax.transAxes,
            ha="center", va="center")

ax.set_xlabel("Generation")
ax.set_ylabel("Median Fitness")

if sexual_n == asexual_n and sexual_n > 0:
    ax.set_title(f"Median Fitness Over Time ({sexual_n} Simulations)")
else:
    ax.set_title(
        f"Median Fitness Over Time "
        f"(Sexual: {sexual_n}, Asexual: {asexual_n})"
    )

ax.grid(True)

if LOG_SCALE:
    ax.set_yscale('log')

if ax.get_legend_handles_labels()[0]:
    ax.legend(loc="lower right", frameon=False)

ax.text(0.02, 0.98, "(A)",
        transform=ax.transAxes,
        fontsize=14,
        fontweight='bold',
        va='top')

plt.tight_layout()
plt.savefig(output, dpi=300)
print(f"Saved: {output}")