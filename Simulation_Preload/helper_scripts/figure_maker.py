import string
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse

# -----------------------------
# Configuration Flags
# -----------------------------

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
        return np.array([]), np.array([]), np.array([])

    if arr.ndim == 1:
        return arr, arr, arr

    median = np.median(arr, axis=0)
    q25 = np.percentile(arr, 25, axis=0)
    q75 = np.percentile(arr, 75, axis=0)
    return median, q25, q75


# -----------------------------
# Command Line Arguments
# -----------------------------

parser = argparse.ArgumentParser(description="Plot fitness results from SLiM simulations.")

parser.add_argument(
    "--sexual_data",
    type=str,
    default="sexual_fitness_over_time.txt",
    help="Path to sexual fitness over time data"
)

parser.add_argument(
    "--asexual_data",
    type=str,
    default="asexual_fitness_over_time.txt",
    help="Path to asexual fitness over time data"
)

parser.add_argument(
    "--output",
    type=str,
    default="fitness_over_time.png",
    help="Path to save the output figure"
)

parser.add_argument(
    "--ymin",
    type=float,
    default=None,
    help="Optional shared y-axis minimum"
)

parser.add_argument(
    "--ymax",
    type=float,
    default=None,
    help="Optional shared y-axis maximum"
)

parser.add_argument(
    "--log_scale",
    action="store_true",
    help="Use log scale for y-axis"
)

parser.add_argument(
    "--boxplot",
    action="store_true",
    help="Enable boxplot for final fitness distribution"
)

parser.add_argument(
    "--no_boxplot",
    action="store_true",
    help="Disable boxplot for final fitness distribution (deprecated; boxplots are off by default)"
)

parser.add_argument(
    "--no_panel_labels",
    action="store_true",
    help="Disable automatic panel labels like (A), (B), ..."
)

args = parser.parse_args()

SHOW_DISTRIBUTION = not args.no_boxplot
BOXPLOT = args.boxplot and SHOW_DISTRIBUTION

SEXUAL_DATA_PATH = args.sexual_data
ASEXUAL_DATA_PATH = args.asexual_data
OUTPUT_PATH = args.output

# -----------------------------
# Load Time-Series Data
# -----------------------------

sexual_data = load_2d_array(SEXUAL_DATA_PATH)
asexual_data = load_2d_array(ASEXUAL_DATA_PATH)

print(f"Sexual fitness_over_time shape: {sexual_data.shape}")
print(f"Asexual fitness_over_time shape: {asexual_data.shape}")

sexual_median, sexual_q25, sexual_q75 = compute_stats(sexual_data)
asexual_median, asexual_q25, asexual_q75 = compute_stats(asexual_data)

sexual_n = sexual_data.shape[0] if sexual_data.ndim == 2 else (1 if sexual_data.size > 0 else 0)
asexual_n = asexual_data.shape[0] if asexual_data.ndim == 2 else (1 if asexual_data.size > 0 else 0)

if MEASURE_FITNESS_GAP:
    if sexual_median.size > 0:
        sexual_median = 1 - sexual_median
    if asexual_median.size > 0:
        asexual_median = 1 - asexual_median

sexual_final_fitness = (
    sexual_data[:, -1] if sexual_data.ndim == 2 and sexual_data.shape[1] > 0
    else np.array([])
)

asexual_final_fitness = (
    asexual_data[:, -1] if asexual_data.ndim == 2 and asexual_data.shape[1] > 0
    else np.array([])
)


# -----------------------------
# Plotting
# -----------------------------

if SHOW_DISTRIBUTION:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    time_ax = axes[0]
    dist_ax = axes[1]
    panel_axes = axes
else:
    fig, time_ax = plt.subplots(1, 1, figsize=(7, 5))
    dist_ax = None
    panel_axes = [time_ax]

# ---- Left Panel: Time-Series

any_time_series = False

if sexual_median.size > 0:
    x = np.arange(1, len(sexual_median) + 1)
    if SCATTER:
        time_ax.scatter(x, sexual_median, label="Sexual", s=4, color=SEXUAL_COLOR)
    else:
        time_ax.plot(x, sexual_median, label="Sexual Median", color=SEXUAL_COLOR)
        time_ax.fill_between(
            x,
            sexual_q25,
            sexual_q75,
            alpha=0.3,
            color=SEXUAL_COLOR,
            label="Sexual IQR"
        )
    any_time_series = True

if asexual_median.size > 0:
    x = np.arange(1, len(asexual_median) + 1)
    if SCATTER:
        time_ax.scatter(x, asexual_median, label="Asexual", s=4, color=ASEXUAL_COLOR)
    else:
        time_ax.plot(x, asexual_median, label="Asexual Median", color=ASEXUAL_COLOR)
        time_ax.fill_between(
            x,
            asexual_q25,
            asexual_q75,
            alpha=0.3,
            color=ASEXUAL_COLOR,
            label="Asexual IQR"
        )
    any_time_series = True

if not any_time_series:
    time_ax.text(0.5, 0.5, "No time-series data",
                 transform=time_ax.transAxes,
                 ha="center", va="center")

time_ax.set_xlabel("Generation")
time_ax.set_ylabel("Median Fitness")

time_ax.yaxis.get_major_formatter().set_useOffset(False)

# ---- Title Logic

if sexual_n == asexual_n and sexual_n > 0:
    time_ax.set_title(f"Median Fitness Over Time ({sexual_n} Simulations)")
elif sexual_n > 0 or asexual_n > 0:
    time_ax.set_title(
        f"Median Fitness Over Time "
        f"(Sexual: {sexual_n}, Asexual: {asexual_n} Simulations)"
    )
else:
    time_ax.set_title("Median Fitness Over Time")

time_ax.grid(True)

if args.log_scale:
    time_ax.set_yscale("log")
    if dist_ax is not None:
        dist_ax.set_yscale("log")

if time_ax.get_legend_handles_labels()[0]:
    time_ax.legend()


# ---- Right Panel: Final Fitness Distribution

if dist_ax is not None:
    any_distribution = False

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
        bp = dist_ax.boxplot(
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

        any_distribution = True

    if not any_distribution:
        dist_ax.text(0.5, 0.5, "No final fitness data",
                     transform=dist_ax.transAxes,
                     ha="center", va="center")

    dist_ax.set_title("Final Fitness Distribution")
    dist_ax.set_xlabel("Simulation Type")
    dist_ax.grid(True, alpha=0.3)

    if dist_ax.get_legend_handles_labels()[0]:
        dist_ax.legend()


# ---- Panel Labels

if not args.no_panel_labels:
    for ax, label in zip(panel_axes, string.ascii_uppercase):
        ax.text(0.02, 0.98, f"({label})",
                transform=ax.transAxes,
                fontsize=14,
                fontweight='bold',
                va='top')


if args.ymin is not None and args.ymax is not None:
    time_ax.set_ylim(args.ymin, args.ymax)
    if dist_ax is not None:
        dist_ax.set_ylim(args.ymin, args.ymax)


plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300)

print(f"Saved: {OUTPUT_PATH}")