import string
import numpy as np
import sys
import matplotlib.pyplot as plt
from pathlib import Path

BOXPLOT = True
LOG_SCALE = False
MEASURE_FITNESS_GAP = False
SCATTER = False
FIT_LINE = False


# -----------------------------
# Safe Loaders
# -----------------------------

def load_2d_array(path: str) -> np.ndarray:
    path_obj = Path(path)

    if not path_obj.exists():
        print(f"Warning: {path} does not exist.")
        return np.empty((0, 0))

    rows = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append([float(x) for x in line.split()])
            except ValueError:
                print(f"Warning: Non-numeric data in {path}, skipping line.")

    if not rows:
        print(f"Warning: {path} is empty.")
        return np.empty((0, 0))

    return np.array(rows, dtype=float)


def safe_loadtxt(path: str) -> np.ndarray:
    path_obj = Path(path)

    if not path_obj.exists():
        print(f"Warning: {path} missing.")
        return np.array([])

    try:
        data = np.loadtxt(path)
        if data.size == 0:
            print(f"Warning: {path} empty.")
            return np.array([])
        return np.atleast_1d(data)
    except Exception:
        print(f"Warning: Could not load {path}.")
        return np.array([])


def compute_stats(arr: np.ndarray):
    if arr.size == 0:
        return np.array([]), np.array([])

    if arr.ndim == 1:
        return arr, np.zeros_like(arr)

    return arr.mean(axis=0), arr.std(axis=0)


# -----------------------------
# Load Time-Series Data
# -----------------------------

sexual_data = load_2d_array("sexual_fitness_over_time.txt")
asexual_data = load_2d_array("asexual_fitness_over_time.txt")

sexual_mean, sexual_std_dev = compute_stats(sexual_data)
asexual_mean, asexual_std_dev = compute_stats(asexual_data)

if MEASURE_FITNESS_GAP:
    if sexual_mean.size > 0:
        sexual_mean = 1 - sexual_mean
    if asexual_mean.size > 0:
        asexual_mean = 1 - asexual_mean


# -----------------------------
# Align Lengths Safely
# -----------------------------

max_len = max(len(sexual_mean), len(asexual_mean))

if max_len == 0:
    print("Error: No time-series data available.")
    sys.exit(0)

cycles = np.arange(1, max_len + 1)

min_len = min(len(sexual_mean), len(asexual_mean))

sexual_mean = sexual_mean[:min_len]
sexual_std_dev = sexual_std_dev[:min_len]
asexual_mean = asexual_mean[:min_len]
asexual_std_dev = asexual_std_dev[:min_len]
cycles = cycles[:min_len]


# -----------------------------
# Optional Curve Fitting
# -----------------------------

if FIT_LINE and min_len > 5:
    try:
        from scipy.optimize import curve_fit

        def model_function(x, a, b, c):
            return a - b * np.exp(-c * x)

        if sexual_mean.size > 0:
            popt, _ = curve_fit(
                model_function, cycles, sexual_mean,
                p0=[1.0, 0.1, 0.001], maxfev=10000
            )
            print(f"Line of best fit (sexual): y = {popt[0]:.4f} - {popt[1]:.4f} * exp(-{popt[2]:.4f} * x)")

        if asexual_mean.size > 0:
            popt, _ = curve_fit(
                model_function, cycles, asexual_mean,
                p0=[1.0, 0.1, 0.001], maxfev=10000
            )
            print(f"Line of best fit (asexual): y = {popt[0]:.4f} - {popt[1]:.4f} * exp(-{popt[2]:.4f} * x)")

    except Exception as e:
        print(f"Curve fitting failed: {e}")


# -----------------------------
# Load Final Fitness Data
# -----------------------------

sexual_final_fitness = safe_loadtxt("sexual_final_fitness.txt")
asexual_final_fitness = safe_loadtxt("asexual_final_fitness.txt")


# -----------------------------
# Plotting
# -----------------------------

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# ---- Left Plot: Mean Fitness Over Time

if min_len > 0:

    if SCATTER:
        if asexual_mean.size > 0:
            axes[0].scatter(cycles, asexual_mean, label="Asexual", s=4)
        if sexual_mean.size > 0:
            axes[0].scatter(cycles, sexual_mean, label="Sexual", s=4)

    else:
        if asexual_mean.size > 0:
            axes[0].plot(cycles, asexual_mean, label="Asexual Mean")
            axes[0].fill_between(
                cycles,
                asexual_mean - asexual_std_dev,
                asexual_mean + asexual_std_dev,
                alpha=0.3,
                label="Asexual ±1 SD"
            )

        if sexual_mean.size > 0:
            axes[0].plot(cycles, sexual_mean, label="Sexual Mean")
            axes[0].fill_between(
                cycles,
                sexual_mean - sexual_std_dev,
                sexual_mean + sexual_std_dev,
                alpha=0.3,
                label="Sexual ±1 SD"
            )

else:
    axes[0].text(0.5, 0.5, "No time-series data",
                 transform=axes[0].transAxes,
                 ha="center", va="center")

axes[0].set_xlabel("Generation")
axes[0].set_ylabel("Mean Fitness")
axes[0].set_title("Mean Fitness Over Time")
axes[0].grid(True)

if LOG_SCALE:
    axes[0].set_yscale('log')

axes[0].legend()


# ---- Right Plot: Final Fitness Distribution

if BOXPLOT and sexual_final_fitness.size > 0 and asexual_final_fitness.size > 0:

    bp = axes[1].boxplot(
        [asexual_final_fitness, sexual_final_fitness],
        tick_labels=["Asexual", "Sexual"],
        patch_artist=True
    )

    for patch in bp["boxes"]:
        patch.set_alpha(0.6)

    for median in bp["medians"]:
        median.set_color("black")
        median.set_linewidth(2)

elif sexual_final_fitness.size > 0 and asexual_final_fitness.size > 0:

    axes[1].hist(asexual_final_fitness, bins=15, alpha=0.6, label="Asexual")
    axes[1].hist(sexual_final_fitness, bins=15, alpha=0.6, label="Sexual")

else:
    axes[1].text(0.5, 0.5, "No final fitness data",
                 transform=axes[1].transAxes,
                 ha="center", va="center")

axes[1].set_title("Final Fitness Distribution")
axes[1].set_xlabel("Simulation Type")
axes[1].grid(True, alpha=0.3)


# ---- Panel Labels

for ax, label in zip(axes.flat, string.ascii_uppercase):
    ax.text(0.02, 0.98, f"({label})",
            transform=ax.transAxes,
            fontsize=14,
            fontweight='bold',
            va='top')


plt.tight_layout()
plt.savefig("fitness_over_time.png", dpi=300)
print("Saved: fitness_over_time.png")