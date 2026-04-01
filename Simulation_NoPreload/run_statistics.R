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

# Phase 2: Test significance of varying recombination and epistasis rates

# Test significance of different recombination rates
tmp = kruskal.test(list(results_list[["sex_ben_epi_100_1.0e-07_20"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_100_1.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_100_1.0e-05_20"]]$X9999,
                        results_list[["sex_ben_epi_100_1.0e-04_20"]]$X9999,
                        results_list[["sex_ben_epi_100_1.0e-03_20"]]$X9999))$p.value
pvals[["recomb_rate_sex"]] = tmp

tmp = wilcox.test(results_list[["sex_ben_epi_100_5.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_100_0_20"]]$X9999)$p.value
pvals[["recomb_5e-6_vs_norecomb"]] = tmp

# Test significance of different epistasis rates in sexual
tmp = kruskal.test(list(results_list[["sex_ben_epi_50_5.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_250_5.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_500_5.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_1000_5.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_10000_5.0e-06_20"]]$X9999))$p.value
pvals[["epistasis_rate_sex"]] = tmp

# Test significance of different epistasis rates in asexual
tmp = kruskal.test(list(results_list[["asex_ben_epi_50_0_20"]]$X9999,
                        results_list[["asex_ben_epi_100_0_20"]]$X9999,
                        results_list[["asex_ben_epi_250_0_20"]]$X9999,
                        results_list[["asex_ben_epi_500_0_20"]]$X9999,
                        results_list[["asex_ben_epi_1000_0_20"]]$X9999,
                        results_list[["asex_ben_epi_10000_0_20"]]$X9999))$p.value
pvals[["epistasis_rate_asex"]] = tmp

# Test significance of different epistasis TAGS in sexual
tmp = kruskal.test(list(results_list[["sex_ben_epi_100_5.0e-06_2"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_5"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_10"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_15"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_20"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_25"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_30"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_50"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_100"]]$X9999))$p.value
pvals[["epistasis_tag_sex"]] = tmp

# Test significance of different epistasis TAGS in asexual
tmp = kruskal.test(list(results_list[["asex_ben_epi_100_0_2"]]$X9999,
                        results_list[["asex_ben_epi_100_0_5"]]$X9999,
                        results_list[["sex_ben_epi_100_5.0e-06_10"]]$X9999,
                        results_list[["asex_ben_epi_100_0_15"]]$X9999,
                        results_list[["asex_ben_epi_100_0_20"]]$X9999,
                        results_list[["asex_ben_epi_100_0_25"]]$X9999,
                        results_list[["asex_ben_epi_100_0_30"]]$X9999,
                        results_list[["asex_ben_epi_100_0_50"]]$X9999,
                        results_list[["asex_ben_epi_100_0_100"]]$X9999))$p.value
pvals[["epistasis_tag_asex"]] = tmp

# Test signifcance of presence vs absence of beneficial mutations for sex
tmp = wilcox.test(results_list[["sex_ben_epi_100_5.0e-06_20"]]$X9999,
                  results_list[["sex_noben_epi_100_5.0e-06_20"]]$X9999)$p.value
pvals[["sex_ben_vs_noben"]] = tmp

# Test signifcance of presence vs absence of beneficial mutations for asex
tmp = wilcox.test(results_list[["asex_ben_epi_100_0_20"]]$X9999,
                  results_list[["asex_noben_epi_100_0_20"]]$X9999)$p.value
pvals[["asex_ben_vs_noben"]] = tmp


# Phase 3: Test sex vs asex at different epistasis values

directions = list()

# Helper function to compare sex vs asex at various epi and tag values
compare_sex_asex = function(epi, tags, pvals, directions, results_list) {
  sex_key  = sprintf("sex_ben_epi_%s_5.0e-06_%s", epi, tags)
  asex_key = sprintf("asex_ben_epi_%s_0_%s", epi, tags)
  name     = sprintf("sex_vs_asex_%s_%s", epi, tags)
  
  sex_vals  = results_list[[sex_key]]$X9999
  asex_vals = results_list[[asex_key]]$X9999
  
  p = wilcox.test(sex_vals, asex_vals)$p.value
  pvals[[name]] = p
  
  diff_med = median(sex_vals) - median(asex_vals)
  directions[[name]] = ifelse(diff_med > 0, "sex", "asex")
  
  list(pvals = pvals, directions = directions)
}

# Test sex vs asex with different epi values (constant tag of 20)
epi_values = c(50, 100, 250, 500, 1000, 10000)

for (epi in epi_values) {
  res = compare_sex_asex(epi, 20, pvals, directions, results_list)
  pvals      = res$pvals
  directions = res$directions
}

# Test sex vs asex with different tag values (constant epi of 100)
tag_values = c(2, 5, 10, 15, 20, 25, 30, 50, 100)

for (tag in tag_values) {
  res = compare_sex_asex(100, tag, pvals, directions, results_list)
  pvals      = res$pvals
  directions = res$directions
}


# Bonferroni threshold
corrected_threshold = THRESHOLD / length(pvals)
cat("Bonferroni corrected threshold:", corrected_threshold, "\n")


# Convert p-values to tibble and save to CSV
pval_table = tibble(
  test = names(pvals),
  p_value = unlist(pvals),
  significant = p_value <= corrected_threshold,
  direction = map_chr(names(pvals), ~ if (.x %in% names(directions)) directions[[.x]] else "-")
)

write_csv(pval_table, "noPreload_results.csv")
}
