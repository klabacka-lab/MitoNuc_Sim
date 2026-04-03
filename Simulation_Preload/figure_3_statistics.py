#!/usr/bin/env python3

import argparse
import csv
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import stats


PANEL_CONFIGS = [
    (1, 2, 100),
    (2, 20, 100),
    (3, 100, 100),
    (4, 20, 50),
    (5, 20, 100),
    (6, 20, 1000),
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

    mean_diff = np.mean(sexual_values) - np.mean(asexual_values)
    median_diff = np.median(sexual_values) - np.median(asexual_values)

    ttest_res = stats.ttest_ind(asexual_values, sexual_values, equal_var=False)
    mw_res = stats.mannwhitneyu(asexual_values, sexual_values, alternative="two-sided")

    return [
        {
            "test": "welch_t_test",
            "p_value": float(ttest_res.pvalue),
            "direction": "sex" if mean_diff > 0 else "asex",
        },
        {
            "test": "mann_whitney_u",
            "p_value": float(mw_res.pvalue),
            "direction": "sex" if median_diff > 0 else "asex",
        },
    ]


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

        panel_rows = summarize_pair(asexual_values, sexual_values)

        for panel_row in panel_rows:
            rows.append(
                {
                    "test": f"panel{panel_index}_{run_id}_{panel_row['test']}",
                    "p_value": panel_row["p_value"],
                    "significant": panel_row["p_value"] <= threshold,
                    "direction": panel_row["direction"],
                }
            )

    corrected_threshold = threshold / len(rows)
    for row in rows:
        row["significant"] = row["p_value"] <= corrected_threshold

    with summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["test", "p_value", "significant", "direction"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote summary CSV: {summary_csv}")
    print(f"Bonferroni corrected threshold: {corrected_threshold}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())