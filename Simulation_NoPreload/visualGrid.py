import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import string

# -----------------------------
# Config
# -----------------------------

SEXUAL_COLOR = "orange"
ASEXUAL_COLOR = "blue"

LOG_SCALE = False
MEASURE_FITNESS_GAP = False

# -----------------------------
# Helpers
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


def compute_stats(arr: np.ndarray):
    if arr.size == 0:
        return np.array([]), np.array([])

    if arr.ndim == 1:
        return arr, np.zeros_like(arr)

    return arr.mean(axis=0), arr.std(axis=0)

# -----------------------------
# Plot function
# -----------------------------

def plot_pair(ax, sexual_file, asexual_file):

    sexual_data = np.atleast_2d(np.loadtxt(sexual_file, delimiter=","))
    asexual_data = np.atleast_2d(np.loadtxt(asexual_file, delimiter=","))

    sexual_mean, sexual_std = compute_stats(sexual_data)
    asexual_mean, asexual_std = compute_stats(asexual_data)

    sexual_label = parse_filename_label(sexual_file)
    asexual_label = parse_filename_label(asexual_file)

    sexual_n = sexual_data.shape[0]
    asexual_n = asexual_data.shape[0]

    if MEASURE_FITNESS_GAP:
        sexual_mean = 1 - sexual_mean
        asexual_mean = 1 - asexual_mean

    # --- Asexual
    if asexual_mean.size > 0:
        x = np.arange(1, len(asexual_mean) + 1)
        ax.plot(x, asexual_mean, color=ASEXUAL_COLOR, label=asexual_label)
        ax.fill_between(
            x,
            asexual_mean - asexual_std,
            asexual_mean + asexual_std,
            alpha=0.3,
            color=ASEXUAL_COLOR
        )

    # --- Sexual
    if sexual_mean.size > 0:
        x = np.arange(1, len(sexual_mean) + 1)
        ax.plot(x, sexual_mean, color=SEXUAL_COLOR, label=sexual_label)
        ax.fill_between(
            x,
            sexual_mean - sexual_std,
            sexual_mean + sexual_std,
            alpha=0.3,
            color=SEXUAL_COLOR
        )

    # Title
    if sexual_n == asexual_n:
        ax.set_title(f"{sexual_n} sims", fontsize=10)
    else:
        ax.set_title(f"S:{sexual_n} A:{asexual_n}", fontsize=10)

    ax.grid(True, alpha=0.3)

    if LOG_SCALE:
        ax.set_yscale("log")

    # Legend bottom-right, no box
    if ax.get_legend_handles_labels()[0]:
        ax.legend(loc="upper right", frameon=False, fontsize=7)

# -----------------------------
# File pairs (6 plots)
# -----------------------------

pairs = [
    ("./NoPreload_Data/sex_ben_epi_100_5.0e-06_2.csv", "./NoPreload_Data/asex_ben_epi_100_0_2.csv"),
    ("./NoPreload_Data/sex_ben_epi_100_5.0e-06_20.csv", "./NoPreload_Data/asex_ben_epi_100_0_20.csv"),
    ("./NoPreload_Data/sex_ben_epi_100_5.0e-06_100.csv", "./NoPreload_Data/asex_ben_epi_100_0_100.csv"),
    ("./NoPreload_Data/sex_ben_epi_50_5.0e-06_20.csv", "./NoPreload_Data/asex_ben_epi_50_0_20.csv"),
    ("./NoPreload_Data/sex_ben_epi_100_5.0e-06_20.csv", "./NoPreload_Data/asex_ben_epi_100_0_20.csv"),
    ("./NoPreload_Data/sex_ben_epi_10000_5.0e-06_20.csv", "./NoPreload_Data/asex_ben_epi_10000_0_20.csv"),
]

# -----------------------------
# Create 2x3 grid
# -----------------------------

fig, axes = plt.subplots(
    2, 3,
    figsize=(12, 8),
    sharex=True,
    sharey=False
)

axes = axes.flatten()

# Plot each pair
for i, (sex_file, asex_file) in enumerate(pairs):
    plot_pair(axes[i], sex_file, asex_file)

# Bottom row → x labels
for ax in axes[3:]:
    ax.set_xlabel("Generation")

# Left column → y labels
for ax in axes[::3]:
    ax.set_ylabel("Fitness")

# Panel labels A–F
for ax, label in zip(axes, string.ascii_uppercase):
    ax.text(0.02, 0.98, f"({label})",
            transform=ax.transAxes,
            fontsize=12,
            fontweight='bold',
            va='top')

plt.tight_layout()
plt.savefig("Sim1GridPlot.png", dpi=300)
