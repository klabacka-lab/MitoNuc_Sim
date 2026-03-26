library(tidyverse)

file_names = list.files(path = "sim_results", pattern = "\\.csv$")
results_list = map(file_names, ~ read_csv(file.path("sim_results", .x), col_names = FALSE))
names(results_list) = str_remove(file_names, "\\.csv$")

saveRDS(results_list, "results_list.rds")
results_list = readRDS("results_list.rds")

{
THRESHOLD = 0.05

# Phase 1: Run Shapiro-Wilk on final generation of each tibble to test normality
  
shapiro_results = map(results_list, ~ shapiro.test(.x[[ncol(.x)]]))

# Bonferroni corrected alpha for all tests
shapiro_alpha = THRESHOLD / length(shapiro_results)

# Split into normal and non-normal
normal = names(shapiro_results)[map_dbl(shapiro_results, ~ .x$p.value) > shapiro_alpha]
non_normal = names(shapiro_results)[map_dbl(shapiro_results, ~ .x$p.value) <= shapiro_alpha]

cat("Normal:", length(normal), "\n")
cat("Non-normal:", length(non_normal), "\n")

# Create empty list to collect p-values
pvals = list()

# Phase 2: Kruskal-Wallis tests to test significance of recombination and epistasis rates

# Test significance of different recombination rates
tmp = kruskal.test(list(results_list[["sex_ben_epi_250_1.0e-06"]]$X9999,
                        results_list[["sex_ben_epi_250_5.0e-06"]]$X9999,
                        results_list[["sex_ben_epi_250_1.0e-05"]]$X9999,
                        results_list[["sex_ben_epi_250_1.0e-04"]]$X9999,
                        results_list[["sex_ben_epi_250_1.0e-03"]]$X9999))$p.value
pvals[["recomb_rate_sex"]] = tmp

# Test significance of different epistasis rates in sexual
tmp = kruskal.test(list(results_list[["sex_ben_epi_100_1.0e-05"]]$X9999,
                        results_list[["sex_ben_epi_250_1.0e-05"]]$X9999,
                        results_list[["sex_ben_epi_500_1.0e-05"]]$X9999,
                        results_list[["sex_ben_epi_1000_1.0e-05"]]$X9999,
                        results_list[["sex_ben_epi_10000_1.0e-05"]]$X9999))$p.value
pvals[["epistasis_rate_sex_recomb1.0e-05"]] = tmp

# Test significance of different epistasis rates in asexual
tmp = kruskal.test(list(results_list[["asex_ben_epi_100_0"]]$X9999,
                        results_list[["asex_ben_epi_250_0"]]$X9999,
                        results_list[["asex_ben_epi_500_0"]]$X9999,
                        results_list[["asex_ben_epi_1000_0"]]$X9999,
                        results_list[["asex_ben_epi_10000_0"]]$X9999))$p.value
pvals[["epistasis_rate_asex"]] = tmp

# Phase 3: Wilcoxon rank-sum tests

# Epistasis presence/absence
tmp = wilcox.test(results_list[["sex_ben_epi_250_1.0e-05"]]$X9999,
                  results_list[["sex_ben_noepi_250_1.0e-05"]]$X9999)$p.value
pvals[["sex_epi_vs_noepi"]] = tmp

tmp = wilcox.test(results_list[["asex_ben_epi_250_0"]]$X9999,
                  results_list[["asex_ben_noepi_250_0"]]$X9999)$p.value
pvals[["asex_epi_vs_noepi"]] = tmp


# Beneficial mutation presence/absence
tmp = wilcox.test(results_list[["sex_ben_epi_250_1.0e-05"]]$X9999,
                  results_list[["sex_noben_epi_250_1.0e-05"]]$X9999)$p.value
pvals[["sex_ben_vs_noben"]] = tmp

tmp = wilcox.test(results_list[["asex_ben_epi_250_0"]]$X9999,
                  results_list[["asex_noben_epi_250_0"]]$X9999)$p.value
pvals[["asex_ben_vs_noben"]] = tmp

# Phase 4: Sex vs asex Wilcoxon tests across epistasis rates

tmp = wilcox.test(results_list[["sex_ben_epi_100_1.0e-05"]]$X9999,
                  results_list[["asex_ben_epi_100_0"]]$X9999)$p.value
pvals[["sex_vs_asex_epi100"]] = tmp

tmp = wilcox.test(results_list[["sex_ben_epi_250_1.0e-05_10000"]]$X9999,
                  results_list[["asex_ben_epi_250_0"]]$X9999)$p.value
pvals[["sex_vs_asex_epi250"]] = tmp

tmp = wilcox.test(results_list[["sex_ben_epi_500_1.0e-05"]]$X9999,
                  results_list[["asex_ben_epi_500_0"]]$X9999)$p.value
pvals[["sex_vs_asex_epi500"]] = tmp


# Bonferroni threshold
corrected_threshold = THRESHOLD / 10
pvals[["bonferroni_threshold"]] = corrected_threshold
cat("Bonferroni corrected threshold:", corrected_threshold, "\n")


# Convert p-values to tibble and save to CSV
pval_table = tibble(
  test = names(pvals),
  p_value = unlist(pvals)
)

write_csv(pval_table, "pvalues_results.csv")
}
