#!/usr/bin/env python3

import argparse
import csv
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


PANEL_CONFIGS = [
    (1, 2, 100),
    (2, 20, 100),
    (3, 100, 100),
    (4, 20, 10),
    (5, 20, 100),
    (6, 20, 10000),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run stat_analysis.py for the figure-3 configuration outputs and "
            "write a combined CSV summary."
        )
    )
    parser.add_argument(
        "--folder",
        type=str,
        default="cached_data/fig_3",
        help="Folder containing sexual_/asexual_ data files from run_fig_3.sh",
    )
    return parser.parse_args()


def load_file(filename: Path) -> np.ndarray:
    try:
        with filename.open("r", encoding="utf-8") as handle:
            lines = [line.strip() for line in handle if line.strip()]

        if not lines:
            return np.array([])

        if any(" " in line for line in lines):
            return np.array([float(line.split()[-1]) for line in lines])

        return np.array([float(line) for line in lines])
    except Exception as exc:
        raise RuntimeError(f"Error reading {filename}: {exc}") from exc


def summarize_pair(asexual_values: np.ndarray, sexual_values: np.ndarray):
    if len(asexual_values) < 3 or len(sexual_values) < 3:
        raise ValueError("Each distribution must have at least 3 data points.")

    median_diff = np.median(sexual_values) - np.median(asexual_values)

    mw_res = stats.mannwhitneyu(asexual_values, sexual_values, alternative="two-sided")

    return {
        "p_value": float(mw_res.pvalue),
        "direction": "sex" if median_diff > 0 else "asex",
    }


def main() -> int:
    args = parse_args()

    script_dir = Path(__file__).resolve().parent
    folder_path = (script_dir / args.folder).resolve()
    stat_script = script_dir / "helper_scripts" / "stat_analysis.py"

    summary_csv = script_dir / "fig3_statistics.csv"
    folder_path.mkdir(parents=True, exist_ok=True)
    summary_csv.parent.mkdir(parents=True, exist_ok=True)

    threshold = 0.05
    rows = []
    wide_rows = []

    for panel_index, num_tags, epi_const in PANEL_CONFIGS:
        run_id = f"tags{num_tags}_epi{epi_const}"
        asexual_file = folder_path / f"asexual_{run_id}_data.txt"
        sexual_file = folder_path / f"sexual_{run_id}_data.txt"

        if not asexual_file.exists():
            raise FileNotFoundError(f"Missing asexual data file: {asexual_file}")
        if not sexual_file.exists():
            raise FileNotFoundError(f"Missing sexual data file: {sexual_file}")

        command = [
            sys.executable,
            str(stat_script),
            "--asexual_data",
            str(asexual_file),
            "--sexual_data",
            str(sexual_file),
        ]

        print("Running:", " ".join(command))
        subprocess.run(command, check=True)

        asexual_values = load_file(asexual_file)
        sexual_values = load_file(sexual_file)

        mw = summarize_pair(asexual_values, sexual_values)

        rows.append(
            {
                "panel": panel_index,
                "num_tags": num_tags,
                "epi_const": epi_const,
                "p_value": mw["p_value"],
                "significant": mw["p_value"] <= threshold,
                "direction": mw["direction"],
            }
        )

        wide_rows.append(
            {
                "config": f"tags{num_tags}_epi{epi_const}",
                "mw_p_value": mw["p_value"],
                "mw_significant": None,
                "mw_direction": mw["direction"],
            }
        )

    corrected_threshold = threshold / len(rows)
    for row in rows:
        row["significant"] = row["p_value"] <= corrected_threshold

    for wide_row in wide_rows:
        wide_row["mw_significant"] = wide_row["mw_p_value"] <= corrected_threshold

    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["panel", "num_tags", "epi_const", "p_value", "significant", "direction"],
        )
        writer.writeheader()
        writer.writerows(rows)

    wide_csv = script_dir / "fig3_statistics_wide.csv"
    with wide_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["config", "mw_p_value", "mw_significant", "mw_direction"],
        )
        writer.writeheader()
        writer.writerows(wide_rows)

    wide_png = script_dir / "fig3_statistics_wide.png"
    _render_wide_table(wide_rows, wide_png)

    print(f"Wrote summary CSV: {summary_csv}")
    print(f"Wrote wide CSV: {wide_csv}")
    print(f"Wrote wide PNG: {wide_png}")
    print(f"Bonferroni corrected threshold: {corrected_threshold}")
    return 0


def _render_wide_table(wide_rows: list, out_path: Path) -> None:
    col_headers = [
        "Config",
        "Mann-Whitney\np-value", "Mann-Whitney\nSignificant?", "Mann-Whitney\nDirection",
    ]

    cell_data = []
    for row in wide_rows:
        cell_data.append([
            row["config"],
            f"{row['mw_p_value']:.4g}",
            str(row["mw_significant"]),
            row["mw_direction"],
        ])

    n_rows = len(cell_data)
    n_cols = len(col_headers)
    row_h = 0.45
    fig_h = row_h * (n_rows + 1) + 0.6
    fig_w = n_cols * 1.55

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.axis("off")

    table = ax.table(
        cellText=cell_data,
        colLabels=col_headers,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.4)

    # Style header row
    for col in range(n_cols):
        cell = table[0, col]
        cell.set_facecolor("#2c3e50")
        cell.set_text_props(color="white", fontweight="bold")
        cell.set_height(cell.get_height() * 2.5)

    # Style data rows
    for row_idx, row in enumerate(cell_data, start=1):
        for col_idx in range(n_cols):
            cell = table[row_idx, col_idx]
            cell.set_facecolor("#eaf0fb" if row_idx % 2 == 0 else "white")
            cell.set_edgecolor("#cccccc")

    ax.set_title(
        "Figure 3 Statistics",
        fontsize=10,
        fontweight="bold",
        pad=8,
    )

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    raise SystemExit(main())