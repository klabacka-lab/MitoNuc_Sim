import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from pathlib import Path
import numpy as np
import subprocess
import argparse
import sys
from matplotlib.lines import Line2D
import string

parser = argparse.ArgumentParser(
    description="Generate Figure 3 panels from simulation output files."
)
parser.add_argument(
    "--folder",
    type=str,
    default="cached_data/fig_3",
    help="Folder containing sexual/asexual data files and where output images are written",
)
args = parser.parse_args()

folder_path = Path(args.folder)
folder_path.mkdir(parents=True, exist_ok=True)
script_dir = Path(__file__).resolve().parent
figure_maker_script = script_dir / "helper_scripts" / "figure_maker.py"

LOG_SCALE = False
Y_SHARE = False

# --------------------------------------------
# Layout: 2 rows x 3 cols
# Row 0: vary epi while tags are fixed at 20
# Row 1: vary tags while epi is fixed at 100
# --------------------------------------------

rows = [
    [(20, 10), (20, 100), (20, 10000)],
    [(2, 100), (20, 100), (100, 100)],
]

row_labels = [
    "Vary epi\n(tags fixed at 20)",
    "Vary tags\n(epi fixed at 100)",
]

# Flat list of unique configs to generate
configs = list({cfg for row in rows for cfg in row})

# --------------------------------------------
# Helper functions
# --------------------------------------------

def run_id(num_tags, epi_const):
    return f"tags{num_tags}_epi{epi_const}"

def sexual_path(num_tags, epi_const):
    return folder_path / f"sexual_{run_id(num_tags, epi_const)}_data.txt"

def asexual_path(num_tags, epi_const):
    return folder_path / f"asexual_{run_id(num_tags, epi_const)}_data.txt"

def plot_path(num_tags, epi_const):
    return folder_path / f"plot_{run_id(num_tags, epi_const)}.png"


def config_label(num_tags, epi_const):
    return f"tags={num_tags}, epi={epi_const}"

def safe_load(path):
    if not path.exists() or path.stat().st_size == 0:
        return None
    try:
        return np.atleast_1d(np.loadtxt(path))
    except Exception:
        return None


def median_iqr_bounds(data):
    """Return lower/upper bounds using the plotted median with IQR envelope."""
    if data is None or data.size == 0:
        return None

    if data.ndim == 1:
        lower = data
        upper = data
    else:
        lower = np.percentile(data, 25, axis=0)
        upper = np.percentile(data, 75, axis=0)

    return lower, upper

# --------------------------------------------
# Step 1 — Load all data ONCE
# --------------------------------------------

data_cache = {}

for num_tags, epi_const in configs:

    sexual_data = safe_load(sexual_path(num_tags, epi_const))
    asexual_data = safe_load(asexual_path(num_tags, epi_const))

    data_cache[(num_tags, epi_const)] = {
        "sexual_data": sexual_data,
        "asexual_data": asexual_data,
    }

# --------------------------------------------
# Step 2 — Compute global y limits ONLY if needed
# --------------------------------------------

global_min = None
global_max = None

if Y_SHARE:
    lower_vals = []
    upper_vals = []

    for cfg in data_cache.values():
        for data in [cfg["sexual_data"], cfg["asexual_data"]]:
            bounds = median_iqr_bounds(data)
            if bounds is None:
                continue
            lower, upper = bounds
            lower_vals.extend(lower.tolist())
            upper_vals.extend(upper.tolist())

    if lower_vals and upper_vals:
        # Shared limits are based on the same plotted metric (median + IQR)
        # and include the full envelope so panel data is never clipped.
        low = float(np.min(lower_vals))
        high = float(np.max(upper_vals))

        span = high - low
        pad = 0.05 * span if span > 0 else max(abs(high) * 0.05, 1e-9)

        global_min = low - pad
        global_max = high + pad

    print("Global y-axis limits:", global_min, global_max)

# --------------------------------------------
# Step 3 — Generate individual plot PNGs
# --------------------------------------------

for num_tags, epi_const in configs:

    cfg = data_cache[(num_tags, epi_const)]

    if cfg["sexual_data"] is None and cfg["asexual_data"] is None:
        print(f"Skipping tags{num_tags} epi{epi_const} (no data)")
        continue

    cmd = [
        sys.executable,
        str(figure_maker_script),
        "--sexual_data", str(sexual_path(num_tags, epi_const)),
        "--asexual_data", str(asexual_path(num_tags, epi_const)),
        "--output", str(plot_path(num_tags, epi_const)),
        "--no_boxplot",
        "--no_panel_labels",
    ]

    if Y_SHARE and global_min is not None and global_max is not None:
        cmd += ["--ymin", str(global_min), "--ymax", str(global_max)]

    if LOG_SCALE:
        cmd.append("--log_scale")

    print("Running:", " ".join(cmd))
    subprocess.run(cmd)

# --------------------------------------------
# Step 4 — Combine PNGs into 2x3 figure
# --------------------------------------------

fig, axes = plt.subplots(2, 3, figsize=(18, 8))
fig.suptitle("Simulation: Preloaded", fontsize=22, fontweight="bold", y=0.98)
fig.subplots_adjust(left=0.08, right=1.0, bottom=0.0, top=0.88, hspace=0.55, wspace=0.0)

placeholder = Image.new("RGB", (200, 200), color=(200, 200, 200))
draw = ImageDraw.Draw(placeholder)
draw.text((50, 90), "Missing", fill=(0, 0, 0))

for i, row in enumerate(rows):
    for j, (num_tags, epi_const) in enumerate(row):

        fname = plot_path(num_tags, epi_const)

        try:
            img = Image.open(fname)
        except FileNotFoundError:
            print(f"Warning: File not found: {fname}")
            img = placeholder

        ax = axes[i, j]
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(config_label(num_tags, epi_const), fontsize=12)
        panel_idx = i * len(row) + j
        ax.text(
            -0.02,
            1.02,
            f"({string.ascii_uppercase[panel_idx]})",
            transform=ax.transAxes,
            fontsize=14,
            fontweight="bold",
            va="top",
            ha="left",
        )

        if j == 0:
            ax.text(
                -0.15, 0.5,
                row_labels[i],
                transform=ax.transAxes,
                fontsize=13,
                va="center",
                ha="right",
            )

top_row_bottom = min(ax.get_position().y0 for ax in axes[0, :])
bottom_row_top = max(ax.get_position().y1 for ax in axes[1, :])
separator_y = (top_row_bottom + bottom_row_top) / 2
separator_x0 = axes[0, 0].get_position().x0
separator_x1 = axes[0, -1].get_position().x1

fig.add_artist(
    Line2D(
        [separator_x0, separator_x1],
        [separator_y, separator_y],
        transform=fig.transFigure,
        color="#666666",
        linewidth=0.8,
        alpha=0.45,
    )
)

plt.savefig("figure_3.png", dpi=300)
