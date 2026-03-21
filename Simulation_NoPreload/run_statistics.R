library(tidyverse)

file_names = list.files(path = "sim_results", pattern = "\\.csv$")
results_list = map(file_names, ~ read_csv(file.path("sim_results", .x), col_names = FALSE))
names(results_list) = str_remove(file_names, "\\.csv$")

saveRDS(results_list, "results_list.rds")
results_list = readRDS("results_list.rds")

THRESHOLD = 0.05

{
# Phase 0: Run Shapiro-Wilk on final generation of each tibble
shapiro_results = map(results_list, ~ shapiro.test(.x[[ncol(.x)]]))

# Bonferroni corrected alpha for 62 tests
shapiro_alpha = THRESHOLD / length(shapiro_results)
cat("Shapiro Bonferroni alpha:", shapiro_alpha, "\n")

# Split into normal and non-normal
normal = names(shapiro_results)[map_dbl(shapiro_results, ~ .x$p.value) > shapiro_alpha]
non_normal = names(shapiro_results)[map_dbl(shapiro_results, ~ .x$p.value) <= shapiro_alpha]

cat("Normal:", length(normal), "\n")
cat("Non-normal:", length(non_normal), "\n")

# Phase 1 - Wilcoxon rank-sum tests

# Epistasis presence/absence
cat("sex epi vs noepi:", wilcox.test(results_list[["sex_ben_epi"]]$X3999,
                                     results_list[["sex_ben_noepi"]]$X3999)$p.value, "\n")
cat("asex epi vs noepi:", wilcox.test(results_list[["asex_ben_epi"]]$X3999,
                                      results_list[["asex_ben_noepi"]]$X3999)$p.value, "\n")

# Beneficial mutation presence/absence
cat("sex ben vs noben:", wilcox.test(results_list[["sex_ben_epi"]]$X3999,
                                     results_list[["sex_noben_epi"]]$X3999)$p.value, "\n")
cat("asex ben vs noben:", wilcox.test(results_list[["asex_ben_epi"]]$X3999,
                                      results_list[["asex_noben_epi"]]$X3999)$p.value, "\n")

# Phase 2 - Kruskal-Wallis tests

# Epistasis rate across four levels (100, 500, 1000, 10000), recombination = 0
cat("Epistasis rate asex:", kruskal.test(list(results_list[["asex_ben_epi_100_0"]]$X3999,
                                              results_list[["asex_ben_epi_500_0"]]$X3999,
                                              results_list[["asex_ben_epi_1000_0"]]$X3999,
                                              results_list[["asex_ben_epi_10000_0"]]$X3999))$p.value, "\n")

# Epistasis rate across four levels (100, 500, 1000, 10000), recombination = 0.0001
cat("Epistasis rate sex (recomb = 0.0001):", kruskal.test(list(results_list[["sex_ben_epi_100_0.0001"]]$X3999,
                                             results_list[["sex_ben_epi_500_0.0001"]]$X3999,
                                             results_list[["sex_ben_epi_1000_0.0001"]]$X3999,
                                             results_list[["sex_ben_epi_10000_0.0001"]]$X3999))$p.value, "\n")

# Epistasis rate across four levels (100, 500, 1000, 10000), recombination = 1e-05
cat("Epistasis rate sex (recomb = 1e-05):", kruskal.test(list(results_list[["sex_ben_epi_100_1.0e-05"]]$X3999,
                                                              results_list[["sex_ben_epi_500_1.0e-05"]]$X3999,
                                                              results_list[["sex_ben_epi_1000_1.0e-05"]]$X3999,
                                                              results_list[["sex_ben_epi_10000_1.0e-05"]]$X3999))$p.value, "\n")

# Recombination rate across four levels (0, 0.0001, 1e-05, 1e-06), epistasis rate = 1000
cat("Recombination rate sex:", kruskal.test(list(results_list[["sex_ben_epi_1000_0.0001"]]$X3999,
                                                 results_list[["sex_ben_epi_1000_1.0e-05"]]$X3999,
                                                 results_list[["sex_ben_epi_1000_1.0e-06"]]$X3999))$p.value, "\n")

# Phase 3 - Sex vs asex Wilcoxon tests across epistasis rates

corrected_threshold = THRESHOLD / 12
}