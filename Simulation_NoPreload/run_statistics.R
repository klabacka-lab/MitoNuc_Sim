library(tidyverse)

file_names = list.files(path = "sim_results", pattern = "\\.csv$")
results_list = map(file_names, ~ read_csv(file.path("sim_results", .x), col_names = FALSE))
names(results_list) = str_remove(file_names, "\\.csv$")

saveRDS(results_list, "results_list.rds")
results_list = readRDS("results_list.rds")

{
THRESHOLD = 0.05

p_vals = list()

# Phase 0: Run Shapiro-Wilk on final generation of each tibble
shapiro_results = map(results_list, ~ shapiro.test(.x[[ncol(.x)]]))

# Bonferroni corrected alpha for 62 tests
shapiro_alpha = THRESHOLD / length(shapiro_results)

# Split into normal and non-normal
normal = names(shapiro_results)[map_dbl(shapiro_results, ~ .x$p.value) > shapiro_alpha]
non_normal = names(shapiro_results)[map_dbl(shapiro_results, ~ .x$p.value) <= shapiro_alpha]

cat("Normal:", length(normal), "\n")
cat("Non-normal:", length(non_normal), "\n")

# Create empty list to collect p-values
pvals = list()

# Phase 1 - Wilcoxon rank-sum tests

# Epistasis presence/absence
tmp = wilcox.test(results_list[["sex_ben_epi"]]$X3999,
                  results_list[["sex_ben_noepi"]]$X3999)$p.value
pvals[["sex_epi_vs_noepi"]] = tmp
cat("sex epi vs noepi:", tmp, "\n")

tmp = wilcox.test(results_list[["asex_ben_epi"]]$X3999,
                  results_list[["asex_ben_noepi"]]$X3999)$p.value
pvals[["asex_epi_vs_noepi"]] = tmp
cat("asex epi vs noepi:", tmp, "\n")


# Beneficial mutation presence/absence
tmp = wilcox.test(results_list[["sex_ben_epi"]]$X3999,
                  results_list[["sex_noben_epi"]]$X3999)$p.value
pvals[["sex_ben_vs_noben"]] = tmp
cat("sex ben vs noben:", tmp, "\n")

tmp = wilcox.test(results_list[["asex_ben_epi"]]$X3999,
                  results_list[["asex_noben_epi"]]$X3999)$p.value
pvals[["asex_ben_vs_noben"]] = tmp
cat("asex ben vs noben:", tmp, "\n")


# Phase 2 - Kruskal-Wallis tests

tmp = kruskal.test(list(results_list[["asex_ben_epi_100_0"]]$X3999,
                        results_list[["asex_ben_epi_500_0"]]$X3999,
                        results_list[["asex_ben_epi_1000_0"]]$X3999,
                        results_list[["asex_ben_epi_10000_0"]]$X3999))$p.value
pvals[["epistasis_rate_asex"]] = tmp
cat("Epistasis rate asex:", tmp, "\n")

tmp = kruskal.test(list(results_list[["sex_ben_epi_100_0.0001"]]$X3999,
                        results_list[["sex_ben_epi_500_0.0001"]]$X3999,
                        results_list[["sex_ben_epi_1000_0.0001"]]$X3999,
                        results_list[["sex_ben_epi_10000_0.0001"]]$X3999))$p.value
pvals[["epistasis_rate_sex_recomb0001"]] = tmp
cat("Epistasis rate sex (recomb = 0.0001):", tmp, "\n")

tmp = kruskal.test(list(results_list[["sex_ben_epi_100_1.0e-05"]]$X3999,
                        results_list[["sex_ben_epi_500_1.0e-05"]]$X3999,
                        results_list[["sex_ben_epi_1000_1.0e-05"]]$X3999,
                        results_list[["sex_ben_epi_10000_1.0e-05"]]$X3999))$p.value
pvals[["epistasis_rate_sex_recomb1e05"]] = tmp
cat("Epistasis rate sex (recomb = 1e-05):", tmp, "\n")

tmp = kruskal.test(list(results_list[["sex_ben_epi_1000_0.0001"]]$X3999,
                        results_list[["sex_ben_epi_1000_1.0e-05"]]$X3999,
                        results_list[["sex_ben_epi_1000_1.0e-06"]]$X3999))$p.value
pvals[["recomb_rate_sex"]] = tmp
cat("Recombination rate sex:", tmp, "\n")


# Phase 3 - Sex vs asex Wilcoxon tests across epistasis rates

tmp = wilcox.test(results_list[["sex_ben_epi_100_1.0e-05_10000"]]$X9999,
                  results_list[["asex_ben_epi_100_1.0e-05_10000"]]$X9999)$p.value
pvals[["sex_vs_asex_epi100"]] = tmp
cat("Sex vs asex (epi = 100):", tmp, "\n")

tmp = wilcox.test(results_list[["sex_ben_epi_500_1.0e-05_10000"]]$X9999,
                  results_list[["asex_ben_epi_500_1.0e-05_10000"]]$X9999)$p.value
pvals[["sex_vs_asex_epi500"]] = tmp
cat("Sex vs asex (epi = 500):", tmp, "\n")

tmp = wilcox.test(results_list[["sex_ben_epi_1000_1.0e-05_10000"]]$X9999,
                  results_list[["asex_ben_epi_1000_1.0e-05_10000"]]$X9999)$p.value
pvals[["sex_vs_asex_epi1000"]] = tmp
cat("Sex vs asex (epi = 1000):", tmp, "\n")


# Bonferroni threshold
corrected_threshold = THRESHOLD / 11
pvals[["bonferroni_threshold"]] = corrected_threshold
cat("Bonferroni corrected threshold:", corrected_threshold, "\n")


# Convert p-values to tibble and save to CSV
pval_table = tibble(
  test = names(pvals),
  p_value = unlist(pvals)
)

write_csv(pval_table, "pvalues_results.csv")
}
