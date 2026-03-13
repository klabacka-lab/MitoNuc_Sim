import string
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse

# -----------------------------
# Configuration Flags
# -----------------------------

BOXPLOT = True
LOG_SCALE = False
MEASURE_FITNESS_GAP = False
SCATTER = False
FIT_LINE = False

SEXUAL_COLOR = "orange"
ASEXUAL_COLOR = "blue"


# -----------------------------
# Safe Loaders
# -----------------------------

def load_2d_array(path: str) -> np.ndarray:
    path_obj = Path(path)

    if not path_obj.exists() or path_obj.stat().st_size == 0:
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
                # Skip partially written lines
                continue

    if not rows:
        return np.empty((0, 0))

    return np.array(rows, dtype=float)


def safe_loadtxt(path: str) -> np.ndarray:
    path_obj = Path(path)

    if not path_obj.exists() or path_obj.stat().st_size == 0:
        return np.array([])

    try:
        data = np.loadtxt(path)
        return np.atleast_1d(data)
    except Exception:
        return np.array([])


def compute_stats(arr: np.ndarray):
    if arr.size == 0:
        return np.array([]), np.array([])

    if arr.ndim == 1:
        return arr, np.zeros_like(arr)
    
    return arr.mean(axis=0), arr.std(axis=0)


# -----------------------------
# Command Line Arguments
# -----------------------------

parser = argparse.ArgumentParser(description="Plot fitness results from SLiM simulations.")
parser.add_argument(
    "--output",
    type=str,
    default="Epi_Reco_Vary_Figures/500Epi_1e-4Recom.png",
    help="Path to save the output figure"
)

args = parser.parse_args()
OUTPUT_PATH = args.output

# -----------------------------
# Load Time-Series Data
# -----------------------------

sexual_data = np.loadtxt("Epi_Reco_Vary_Trials/sex_ben_epi_500_0.0001.csv", delimiter=",")
asexual_data = np.loadtxt("Epi_Reco_Vary_Trials/asex_ben_epi_500_0.csv", delimiter=",")

print(f"Sexual fitness_over_time shape: {sexual_data.shape}")
print(f"Sexual No Recombination fitness_over_time shape: {asexual_data.shape}")

sexual_mean, sexual_std_dev = compute_stats(sexual_data)
asexual_mean, asexual_std_dev = compute_stats(asexual_data)


# 95% confidence intervals
sexual_ci = np.zeros_like(sexual_mean)
asexual_ci = np.zeros_like(asexual_mean)




sexual_n = sexual_data.shape[0] if sexual_data.ndim == 2 else (1 if sexual_data.size > 0 else 0)
asexual_n = asexual_data.shape[0] if asexual_data.ndim == 2 else (1 if asexual_data.size > 0 else 0)


if sexual_n > 0:
    sexual_ci = 1.96 * sexual_std_dev / np.sqrt(sexual_n)

if asexual_n > 0:
    asexual_ci = 1.96 * asexual_std_dev / np.sqrt(asexual_n)


if MEASURE_FITNESS_GAP:
    if sexual_mean.size > 0:
        sexual_mean = 1 - sexual_mean
    if asexual_mean.size > 0:
        asexual_mean = 1 - asexual_mean


# -----------------------------
# Optional Curve Fitting
# -----------------------------

if FIT_LINE:
    try:
        from scipy.optimize import curve_fit

        def model_function(x, a, b, c):
            return a - b * np.exp(-c * x)

        if sexual_mean.size > 5:
            x = np.arange(1, len(sexual_mean) + 1)
            popt, _ = curve_fit(model_function, x, sexual_mean,
                                p0=[1.0, 0.1, 0.001], maxfev=10000)
            print(f"Sexual fit: y = {popt[0]:.4f} - {popt[1]:.4f} * exp(-{popt[2]:.4f} * x)")

        if asexual_mean.size > 5:
            x = np.arange(1, len(asexual_mean) + 1)
            popt, _ = curve_fit(model_function, x, asexual_mean,
                                p0=[1.0, 0.1, 0.001], maxfev=10000)
            print(f"Asexual fit: y = {popt[0]:.4f} - {popt[1]:.4f} * exp(-{popt[2]:.4f} * x)")

    except Exception as e:
        print(f"Curve fitting failed: {e}")


# -----------------------------
# Load Final Fitness Data
# -----------------------------

# sexual_final_fitness = safe_loadtxt("sexual_final_fitness.txt")
sexual_final_fitness = sexual_data[:, -1]
asexual_final_fitness = asexual_data[:,-1]


# -----------------------------
# Plotting
# -----------------------------

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ---- Left Panel: Time-Series

any_time_series = False



if asexual_mean.size > 0:
    x = np.arange(1, len(asexual_mean) + 1)
    if SCATTER:
        axes[0].scatter(x, asexual_mean, label="Asexual", s=4, color=ASEXUAL_COLOR)
    else:
        axes[0].plot(x, asexual_mean, label="Asexual Mean", color=ASEXUAL_COLOR)
        axes[0].fill_between(
            x,
            asexual_mean - asexual_std_dev,
            asexual_mean + asexual_std_dev,
            alpha=0.3,
            color=ASEXUAL_COLOR,
            label="Asexual ± 1 SD"
        )
    any_time_series = True


if sexual_mean.size > 0:
    x = np.arange(1, len(sexual_mean) + 1)
    if SCATTER:
        axes[0].scatter(x, sexual_mean, label="Sexual", s=4, color=SEXUAL_COLOR)
    else:
        axes[0].plot(x, sexual_mean, label="Sexual Mean", color=SEXUAL_COLOR)
        axes[0].fill_between(
            x,
            sexual_mean - sexual_std_dev,
            sexual_mean + sexual_std_dev,
            alpha=0.3,
            color=SEXUAL_COLOR,
            label="Sexual ± 1 SD"
        )
    any_time_series = True

if not any_time_series:
    axes[0].text(0.5, 0.5, "No time-series data",
                 transform=axes[0].transAxes,
                 ha="center", va="center")

axes[0].set_xlabel("Generation")
axes[0].set_ylabel("Mean Fitness")

# ---- Title Logic

if sexual_n == asexual_n and sexual_n > 0:
    axes[0].set_title(f"Mean Fitness Over Time ({sexual_n} Simulations)")
elif sexual_n > 0 or asexual_n > 0:
    axes[0].set_title(
        f"Mean Fitness Over Time "
        f"(Sexual: {sexual_n}, Asexual: {asexual_n} Simulations)"
    )
else:
    axes[0].set_title("Mean Fitness Over Time")

axes[0].grid(True)

if LOG_SCALE:
    axes[0].set_yscale('log')

if axes[0].get_legend_handles_labels()[0]:
    axes[0].legend()


# ---- Right Panel: Final Fitness Distribution
any_distribution = False

# Always prepare arrays, even if one is empty
box_data = []
tick_labels = []

if asexual_final_fitness.size > 0:
    box_data.append(asexual_final_fitness)
    tick_labels.append("Asexual")
else:
    box_data.append([])
    tick_labels.append("Asexual")

if sexual_final_fitness.size > 0:
    box_data.append(sexual_final_fitness)
    tick_labels.append("Sexual")
else:
    box_data.append([])
    tick_labels.append("Sexual")

if BOXPLOT:
    bp = axes[1].boxplot(
        box_data,
        patch_artist=True,
        tick_labels=tick_labels
    )

    # Set locked colors
    colors = [ASEXUAL_COLOR, SEXUAL_COLOR]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    for median in bp["medians"]:
        median.set_color("black")
        median.set_linewidth(2)

    any_distribution = True

else:
    # Fallback to histogram if BOXPLOT is False
    if asexual_final_fitness.size > 0:
        axes[1].hist(asexual_final_fitness, bins=15,
                     alpha=0.6, label="Asexual", color=ASEXUAL_COLOR)
        any_distribution = True

    if sexual_final_fitness.size > 0:
        axes[1].hist(sexual_final_fitness, bins=15,
                     alpha=0.6, label="Sexual", color=SEXUAL_COLOR)
        any_distribution = True

if not any_distribution:
    axes[1].text(0.5, 0.5, "No final fitness data",
                 transform=axes[1].transAxes,
                 ha="center", va="center")
axes[1].set_title("Fitness Distribution After 4000 Generations")
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
plt.savefig(OUTPUT_PATH, dpi=300)
print(f"Saved: {OUTPUT_PATH}")