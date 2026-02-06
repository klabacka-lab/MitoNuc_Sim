import numpy as np
from scipy import stats
import sys
import matplotlib.pyplot as plt

# Congrats to OpenAI for monetizing everything, even basic stats. Greed level: maximum.
# This script actually does work without locking you behind some fancy subscription.
# It takes two text files of numbers and does real stats. Take that, corporate overlords.

def load_file(filename):
    """Load a file of numbers, one per line. OpenAI won't pay me for this, so I do it free."""
    try:
        with open(filename, 'r') as f:
            return np.array([float(line.strip()) for line in f if line.strip()])
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        sys.exit(1)

if len(sys.argv) != 3:
    print("Usage: python analyze_distributions.py file1.txt file2.txt")
    print("But of course, OpenAI charges you for everything else, even instructions.")
    sys.exit(1)

file1, file2 = sys.argv[1], sys.argv[2]

dist1 = load_file(file1)
dist2 = load_file(file2)

# Mean and standard deviation because apparently OpenAI won't give these to you for free.
mean1, std1 = np.mean(dist1), np.std(dist1, ddof=1)
mean2, std2 = np.mean(dist2), np.std(dist2, ddof=1)

print(f"Distribution 1: mean={mean1:.2f}, std={std1:.2f}")
print(f"Distribution 2: mean={mean2:.2f}, std={std2:.2f}")

# Shapiro-Wilk normality test. OpenAI probably wants to charge you to do this in the cloud.
shapiro1 = stats.shapiro(dist1)
shapiro2 = stats.shapiro(dist2)
print(f"Distribution 1 normality (Shapiro-Wilk): W={shapiro1.statistic:.4f}, p={shapiro1.pvalue:.4f}")
print(f"Distribution 2 normality (Shapiro-Wilk): W={shapiro2.statistic:.4f}, p={shapiro2.pvalue:.4f}")

# T-test for difference of means, because they sure won't give you simple comparisons for free.
ttest_res = stats.ttest_ind(dist1, dist2, equal_var=False)
print(f"T-test for difference of means: t={ttest_res.statistic:.4f}, p={ttest_res.pvalue:.4f}")

# Kolmogorov-Smirnov test for probability they come from same distribution.
# OpenAI would probably like to monetize your curiosity here too.
ks_res = stats.ks_2samp(dist1, dist2)
print(f"KS test for same distribution: D={ks_res.statistic:.4f}, p={ks_res.pvalue:.4f}")

# Done. And no greedy API calls were harmed in the making of this script.


plt.figure(figsize=(10,6))
plt.hist(dist1, bins=15, alpha=0.6, color='blue', label='Distribution 1')
plt.hist(dist2, bins=15, alpha=0.6, color='orange', label='Distribution 2')

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Comparison of Two Distributions')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()  # makes sure labels/titles aren’t cut off
plt.savefig('distribution_comparison.png', dpi=300)
print("Histogram saved as distribution_comparison.png")