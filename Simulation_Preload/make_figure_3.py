import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from pathlib import Path
import numpy as np
import subprocess
import argparse
import sys
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
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
parser.add_argument(
    "--fig_2_instead",
    action="store_true",
    help="Use Simulation_NoPreload CSV inputs (Figure 2 layout/inputs) instead of default Figure 3 TXT inputs",
)
parser.add_argument(
    "--inset_non_y_share_preview",
    action="store_true",
    help="Insert a small non-y-shared raw-lines preview in the upper-right of each panel",
)
args = parser.parse_args()

folder_path = Path(args.folder)
folder_path.mkdir(parents=True, exist_ok=True)
script_dir = Path(__file__).resolve().parent
fig2_data_dir = script_dir.parent / "Simulation_NoPreload" / "NoPreload_Data"
figure_maker_script = script_dir / "helper_scripts" / "figure_maker.py"

LOG_SCALE = False
Y_SHARE = True

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
    "Site Spacing",
    "Tag Amount",
]

# Flat list of unique configs to generate
configs = list({cfg for row in rows for cfg in row})

# --------------------------------------------
# Helper functions
# --------------------------------------------

def run_id(num_tags, epi_const):
    return f"tags{num_tags}_epi{epi_const}"

def sexual_path(num_tags, epi_const):
    if args.fig_2_instead:
        return fig2_data_dir / f"sex_ben_epi_{epi_const}_5.0e-06_{num_tags}.csv"
    return folder_path / f"sexual_{run_id(num_tags, epi_const)}_data.txt"

def asexual_path(num_tags, epi_const):
    if args.fig_2_instead:
        return fig2_data_dir / f"asex_ben_epi_{epi_const}_0_{num_tags}.csv"
    return folder_path / f"asexual_{run_id(num_tags, epi_const)}_data.txt"

def plot_path(num_tags, epi_const):
    return folder_path / f"plot_{run_id(num_tags, epi_const)}.png"


def preview_plot_path(num_tags, epi_const):
    return folder_path / f"plot_preview_{run_id(num_tags, epi_const)}.png"


def config_label(num_tags, epi_const):
    return f"tags={num_tags}, epi={epi_const}"

def safe_load(path):
    if not path.exists() or path.stat().st_size == 0:
        return None
    try:
        delimiter = "," if path.suffix.lower() == ".csv" else None
        return np.atleast_1d(np.loadtxt(path, delimiter=delimiter))
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
        "--no_legend",
    ]

    if Y_SHARE and global_min is not None and global_max is not None:
        cmd += ["--ymin", str(global_min), "--ymax", str(global_max)]

    if LOG_SCALE:
        cmd.append("--log_scale")

    print("Running:", " ".join(cmd))
    subprocess.run(cmd)

    if args.inset_non_y_share_preview:
        preview_cmd = [
            sys.executable,
            str(figure_maker_script),
            "--sexual_data", str(sexual_path(num_tags, epi_const)),
            "--asexual_data", str(asexual_path(num_tags, epi_const)),
            "--output", str(preview_plot_path(num_tags, epi_const)),
            "--no_boxplot",
            "--no_panel_labels",
            "--no_legend",
            "--raw_lines_preview",
        ]

        if LOG_SCALE:
            preview_cmd.append("--log_scale")

        print("Running preview:", " ".join(preview_cmd))
        subprocess.run(preview_cmd)

# --------------------------------------------
# Step 4 — Combine PNGs into 2x3 figure
# --------------------------------------------

fig, axes = plt.subplots(2, 3, figsize=(18, 8))
if args.fig_2_instead:
    fig.suptitle("GMAS", fontsize=22, fontweight="bold", y=0.98)
else:
    fig.suptitle("IMDeS", fontsize=22, fontweight="bold", y=0.98)
fig.subplots_adjust(left=0.08, right=1.0, bottom=0.07, top=0.88, hspace=0.15, wspace=0.0)

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

        if args.inset_non_y_share_preview:
            preview_fname = preview_plot_path(num_tags, epi_const)
            try:
                preview_img = Image.open(preview_fname)
                inset_ax = ax.inset_axes([0.12, 0.58, 0.34, 0.34])
                inset_ax.imshow(preview_img)
                inset_ax.set_xticks([])
                inset_ax.set_yticks([])
                inset_ax.set_facecolor("white")
                for spine in inset_ax.spines.values():
                    spine.set_color("#333333")
                    spine.set_linewidth(0.8)
            except FileNotFoundError:
                print(f"Warning: Preview file not found: {preview_fname}")

top_row_bottom = min(ax.get_position().y0 for ax in axes[0, :])
bottom_row_top = max(ax.get_position().y1 for ax in axes[1, :])
separator_y = (top_row_bottom + bottom_row_top) / 2 + 0.01
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

SEXUAL_COLOR = "orange"
ASEXUAL_COLOR = "blue"

legend_handles = [
    Line2D([0], [0], color=SEXUAL_COLOR, linewidth=2, label="Sexual Median"),
    Patch(facecolor=SEXUAL_COLOR, alpha=0.3, label="Sexual IQR"),
    Line2D([0], [0], color=ASEXUAL_COLOR, linewidth=2, label="Asexual Median"),
    Patch(facecolor=ASEXUAL_COLOR, alpha=0.3, label="Asexual IQR"),
]

fig.legend(
    handles=legend_handles,
    loc="lower center",
    ncol=4,
    fontsize=11,
    frameon=True,
    bbox_to_anchor=(0.5, 0.0),
)

final_output = "figure_2.png" if args.fig_2_instead else "figure_3.png"
plt.savefig(final_output, dpi=300)
