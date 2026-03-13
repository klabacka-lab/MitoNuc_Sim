import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from pathlib import Path
import numpy as np
import subprocess

mutation_profiles = [1, 2, 3]
mutation_labels = {
    1: "1 (Ben+Del)",
    2: "2 (Del)",
    3: "3 (None)"
}

preloads = ["mito", "nucl"]
epis = ["F", "T"]

folder = "automatic_figures/2000"
folder_path = Path(folder)


LOG_SCALE = True

# --------------------------------------------
# Build configuration list
# --------------------------------------------

configs = [
    (mut, preload, epi)
    for mut in mutation_profiles
    for preload in preloads
    for epi in epis
]

# --------------------------------------------
# Helper functions
# --------------------------------------------

def sexual_path(mut, preload, epi):
    return folder_path / f"sexual_mut{mut}_preload_{preload}_epi{epi}_data.txt"

def asexual_path(mut, preload, epi):
    return folder_path / f"asexual_mut{mut}_preload_{preload}_epi{epi}_data.txt"

def plot_path(mut, preload, epi):
    return folder_path / f"plot_mut{mut}_preload_{preload}_epi{epi}.png"

def safe_load(path):
    if not path.exists() or path.stat().st_size == 0:
        return None
    try:
        return np.atleast_1d(np.loadtxt(path))
    except Exception:
        return None

# --------------------------------------------
# Step 1 — Determine global y-axis
# --------------------------------------------

global_min = float("inf")
global_max = float("-inf")

for mut, preload, epi in configs:

    for f in [sexual_path(mut, preload, epi),
              asexual_path(mut, preload, epi)]:

        data = safe_load(f)
        if data is None:
            continue

        global_min = min(global_min, np.min(data))
        global_max = max(global_max, np.max(data))

print("Global y-axis limits:", global_min, global_max)

# --------------------------------------------
# Step 2 — Generate figures
# --------------------------------------------

for mut, preload, epi in configs:

    sexual_file = sexual_path(mut, preload, epi)
    asexual_file = asexual_path(mut, preload, epi)

    sexual_exists = sexual_file.exists() and sexual_file.stat().st_size > 0
    asexual_exists = asexual_file.exists() and asexual_file.stat().st_size > 0

    # Skip if BOTH are missing
    if not sexual_exists and not asexual_exists:
        print(f"Skipping mut{mut} {preload} epi{epi} (no data)")
        continue

    cmd = [
        "python",
        "figure_maker.py",
        "--sexual_data", str(sexual_file),
        "--asexual_data", str(asexual_file),
        "--output", str(plot_path(mut, preload, epi)),
        "--ymin", str(global_min),
        "--ymax", str(global_max)
    ]

    if LOG_SCALE:
        cmd.append("--log_scale")

    print("Running:", " ".join(cmd))
    subprocess.run(cmd)

# --------------------------------------------
# Step 3 — Combine PNGs
# --------------------------------------------

fig, axes = plt.subplots(3, 4, figsize=(16, 12))

placeholder = Image.new("RGB", (200, 200), color=(200, 200, 200))
draw = ImageDraw.Draw(placeholder)
draw.text((50, 90), "Missing", fill=(0, 0, 0))

for i, mut in enumerate(mutation_profiles):

    for j, (preload, epi) in enumerate(
        [(p, e) for p in preloads for e in epis]
    ):

        fname = plot_path(mut, preload, epi)

        try:
            img = Image.open(fname)
        except FileNotFoundError:
            print(f"Warning: File not found: {fname}")
            img = placeholder

        ax = axes[i, j]
        ax.imshow(img)
        ax.axis("off")

        if i == 0:
            ax.set_title(f"{preload} | epi {epi}", fontsize=12)

        if j == 0:
            ax.text(
                -0.15, 0.5,
                mutation_labels[mut],
                transform=ax.transAxes,
                fontsize=14,
                va="center",
                ha="right"
            )

fig.text(0.02, 0.5, "Mutation Profile", va='center',
         rotation='vertical', fontsize=16)

plt.tight_layout(rect=[0.06, 0, 1, 1])
plt.savefig(folder_path / "combined_comparison.png", dpi=300)
plt.show()