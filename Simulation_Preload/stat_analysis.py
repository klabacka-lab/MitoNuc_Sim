import numpy as np
from scipy import stats
import sys
import matplotlib.pyplot as plt
from pathlib import Path


def load_file(filename):
    """Load a file of numbers, keeping only the last value in each row if it's a 2D array."""
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            for line in lines:
                if ' ' in line:
                    return np.array([float(line.split()[-1]) for line in lines])
            return np.array([float(line) for line in lines])
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        sys.exit(1)


def format_p(p):
    return "p < 0.0001" if p < 1e-4 else f"p = {p:.4f}"


def interpret_normality(p):
    return "is consistent with normality" if p > 0.05 else "deviates from normality"


def interpret_difference(p):
    return "a statistically significant difference" if p < 0.05 else "no statistically significant difference"


def generate_summary(mean1, mean2, std1, std2, shapiro1, shapiro2, ttest, mw):
    summary = []

    summary.append(
        f"Distribution 1 (Asexual) has a mean of {mean1:.2f} (SD = {std1:.2f}), "
        f"\nDistribution 2 (Sexual) has a mean of {mean2:.2f} (SD = {std2:.2f})."
    )

    summary.append(
        f"Normality testing: \nDistribution 1 (Asexual) {interpret_normality(shapiro1.pvalue)} "
        f"({format_p(shapiro1.pvalue)}) \nDistribution 2 (Sexual) "
        f"{interpret_normality(shapiro2.pvalue)} ({format_p(shapiro2.pvalue)})."
    )

    summary.append(
        f"The Welch t-test indicates {interpret_difference(ttest.pvalue)} between the means "
        f"({format_p(ttest.pvalue)})."
    )

    summary.append(
        f"The Mann–Whitney U test suggests {interpret_difference(mw.pvalue)} "
        f"between the overall distributions ({format_p(mw.pvalue)})."
    )

    return "\n\n".join(summary)



if len(sys.argv) != 4:
    print("Usage: python stat_analysis.py file1.txt file2.txt output.png")
    sys.exit(1)

file1, file2, output_png = sys.argv[1], sys.argv[2], sys.argv[3]

# ensure output directory exists
Path(output_png).parent.mkdir(parents=True, exist_ok=True)

dist1 = load_file(file1)
dist2 = load_file(file2)

mean1, std1 = np.mean(dist1), np.std(dist1, ddof=1)
mean2, std2 = np.mean(dist2), np.std(dist2, ddof=1)

print(f"Distribution 1 (Asexual): mean={mean1:.2f}, std={std1:.2f}")
print(f"Distribution 2 (Sexual): mean={mean2:.2f}, std={std2:.2f}")

shapiro1 = stats.shapiro(dist1)
shapiro2 = stats.shapiro(dist2)
print(f"Distribution 1 (Asexual) normality (Shapiro-Wilk): W={shapiro1.statistic:.4f}, p={shapiro1.pvalue:.4f}")
print(f"Distribution 2 (Sexual) normality (Shapiro-Wilk): W={shapiro2.statistic:.4f}, p={shapiro2.pvalue:.4f}")

ttest_res = stats.ttest_ind(dist1, dist2, equal_var=False)
print(f"T-test for difference of means: t={ttest_res.statistic:.4f}, p={ttest_res.pvalue:.4f}")

mw_res = stats.mannwhitneyu(dist1, dist2, alternative='two-sided')
print(f"Mann-Whitney U test: U={mw_res.statistic:.4f}, p={mw_res.pvalue:.4f}")

summary = generate_summary(mean1, mean2, std1, std2, shapiro1, shapiro2, ttest_res, mw_res)
print("\nSummary:")
print(summary)

plt.figure(figsize=(10, 6))
plt.hist(dist1, bins=15, alpha=0.6, label='Distribution 1 (Asexual)')
plt.hist(dist2, bins=15, alpha=0.6, label='Distribution 2 (Sexual)')

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Comparison of Two Distributions')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_png, dpi=300)
print(f"Histogram saved as {output_png}")
