import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

mutation_profiles = [1, 2, 3]
mutation_labels = {
    1: "1 (Ben+Del)",
    2: "2 (Del)",
    3: "3 (None)"
}

preloads = ["mito", "nucl"]
epis = ["F", "T"]

folder = "2000"

# Create figure and axes
fig, axes = plt.subplots(3, 4, figsize=(16, 12))

# Generate placeholder image for missing files
placeholder = Image.new("RGB", (200, 200), color=(200, 200, 200))
draw = ImageDraw.Draw(placeholder)
draw.text((50, 90), "Missing", fill=(0, 0, 0))

for i, mut in enumerate(mutation_profiles):
    col = 0
    for preload in preloads:
        for epi in epis:
            fname = f"{folder}/plot_mut{mut}_preload[{preload}]_epi{epi}.png"
            try:
                img = Image.open(fname)
            except FileNotFoundError:
                print(f"Warning: File not found: {fname}")
                img = placeholder

            ax = axes[i, col]
            ax.imshow(img)
            ax.axis("off")

            # Column titles
            if i == 0:
                ax.set_title(f"{preload} | epi {epi}", fontsize=12)

            # Row labels (manual placement)
            if col == 0:
                ax.text(
                    -0.15, 0.5,
                    mutation_labels[mut],
                    transform=ax.transAxes,
                    fontsize=14,
                    va="center",
                    ha="right"
                )

            col += 1

# Main vertical label
fig.text(0.02, 0.5, "Mutation Profile", va='center', rotation='vertical', fontsize=16)

plt.tight_layout(rect=[0.06, 0, 1, 1])
plt.savefig(f"{folder}/combined_comparison.png", dpi=300)
plt.show()
