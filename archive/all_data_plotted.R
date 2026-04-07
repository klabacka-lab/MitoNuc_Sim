library(ggplot2)
library(dplyr)
library(gridExtra)

setwd('/Users/r_klabacka/Documents/UtahTech/Research/MitoNucSimulations')

## PEAK FITNESS DATA

# Obtain the compensatory fitness data
dat_CT_all <- read.csv('data_CompensatoryTest.csv')

# Assuming your dataframe is called dat_CT_all
dat_CT_all_summary <- dat_CT_all %>%
  group_by(SpecificModel, Locus, MitoMutEffect) %>%
  summarise( mean_fitness = mean(FinalFitness),
    sem_fitness = sd(FinalFitness) / sqrt(n()),
    .groups = "drop"
  )

# Create the plot with means and SEM error bars
CT_plot <- ggplot(dat_CT_all_summary, aes(x = SpecificModel, y = mean_fitness, color = MitoMutEffect, group = MitoMutEffect)) +
  geom_point(size = 1) +  # Plot the mean points
   scale_color_manual(values = c("black", "#B7BBBA")) +
  geom_errorbar(aes(ymin = mean_fitness - sem_fitness, ymax = mean_fitness + sem_fitness), width = 0.2) +  # Add error bars
  facet_wrap(~ Locus, scales = "free_x") +  # Faceting by Locus
  theme_minimal() +
  labs(title = "Mean FinalFitness with SEM by SpecificModel, Locus, and MitoMutEffect",
       x = "Specific Model", y = "Mean Final Fitness") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Angle X-axis labels for readability

# Obtain the peak fitness data
dat_PF_all <- read.csv('data_PeakFitness.csv')

# Assuming your dataframe is called dat_CT_all
dat_PF_all_summary <- dat_PF_all %>%
  group_by(SpecificModel, Locus, MitoMutEffect) %>%
  summarise(
    mean_time = mean(EndTime),
    sem_time= sd(EndTime) / sqrt(n()),
    .groups = "drop"
  )

# Create the plot with means and SEM error bars
PF_plot <- ggplot(dat_PF_all_summary, aes(x = SpecificModel, y = mean_time, color = MitoMutEffect, group = MitoMutEffect)) +
  geom_point(size = 1) +  # Plot the mean points
   scale_color_manual(values = c("black", "#B7BBBA")) +
  geom_errorbar(aes(ymin = mean_time - sem_time, ymax = mean_time + sem_time), width = 0.2) +  # Add error bars
  facet_wrap(~ Locus, scales = "free_x") +  # Faceting by Locus
  theme_minimal() +
  labs(title = "Mean EndTime with SEM by SpecificModel, Locus, and MitoMutEffect",
       x = "Specific Model", y = "Mean Final time") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Angle X-axis labels for readability

# subset data
dat_CT_subset <- dat_CT_all %>% filter(Mode %in% c("Asex","Sex", "Haploid") & MitoMutEffect == "Del")
dat_PF_subset <- dat_PF_all %>% filter(Mode %in% c("Asex","Sex", "Haploid") & MitoMutEffect == "Del")

dat_CT_subset_summary <- dat_CT_subset %>%
  group_by(Mode, Locus, MitoMutEffect) %>%
  summarise(
    CT_subset_mean_fitness = mean(FinalFitness),
    CT_subset_sem_fitness= sd(FinalFitness) / sqrt(n()),
    .groups = "drop"
  )

dat_CT_subset$Mode <- factor(dat_CT_subset$Mode, levels = c("Asex", "Sex", "Haploid"))
dat_CT_subset_summary$Mode <- factor(dat_CT_subset_summary$Mode, levels = c("Asex", "Sex", "Haploid"))

CT_subset_plot_with_lines <- ggplot(dat_CT_subset, aes(x = Locus, y = FinalFitness, color = Mode)) +
  # Jittered points with low alpha in the background
  geom_jitter(aes(shape = Mode), width = 0.2, size = 2, alpha = 0.03) +
  # Line to connect the means between groups
  geom_line(data = dat_CT_subset_summary, aes(x = Locus, y = CT_subset_mean_fitness, group = 1, color = Mode), size = 1) +
   scale_color_manual(values = c("#A9DBB8", "#5D87F7", "#DA58A5")) +
  # Add points for the means (if needed)
  geom_point(data = dat_CT_subset_summary, aes(x = Locus, y = CT_subset_mean_fitness, color = Mode), size = 4) +
  facet_wrap(~ Mode, scales = "free_x", strip.position = "top") +  # Faceting by Mode
  theme_minimal() +
  labs(title = "Dot Plot with Averages Connected by Lines",
       x = "Locus", y = "Final Fitness") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),  # Angle x-axis labels for readability
        strip.background = element_blank(),  # Remove background from facet labels
        strip.text = element_text(size = 12))  # Adjust size of facet labels


dat_PF_subset_summary <- dat_PF_subset %>%
  group_by(Mode, Locus, MitoMutEffect) %>%
  summarise(
    PF_subset_mean_time = mean(EndTime),
    PF_subset_sem_time= sd(EndTime) / sqrt(n()),
    .groups = "drop"
  )

dat_PF_subset$Mode <- factor(dat_PF_subset$Mode, levels = c("Asex", "Sex", "Haploid"))
dat_PF_subset_summary$Mode <- factor(dat_PF_subset_summary$Mode, levels = c("Asex", "Sex", "Haploid"))

PF_subset_plot_with_lines <- ggplot(dat_PF_subset, aes(x = Locus, y = EndTime, color = Mode)) +
  # Jittered points with low alpha in the background
  geom_jitter(aes(shape = Mode), width = 0.2, size = 2, alpha = 0.03) +
  # Line to connect the means between groups
  geom_line(data = dat_PF_subset_summary, aes(x = Locus, y = PF_subset_mean_time, group = 1, color = Mode), size = 1) +
   scale_color_manual(values = c("#A9DBB8", "#5D87F7", "#DA58A5")) +
  # Add points for the means (if needed)
  geom_point(data = dat_PF_subset_summary, aes(x = Locus, y = PF_subset_mean_time, color = Mode), size = 4) +
  facet_wrap(~ Mode, scales = "free_x", strip.position = "top") +  # Faceting by Mode
  theme_minimal() +
  labs(title = "Dot Plot with Averages Connected by Lines",
       x = "Locus", y = "Final time") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),  # Angle x-axis labels for readability
        strip.background = element_blank(),  # Remove background from facet labels
        strip.text = element_text(size = 12))  # Adjust size of facet labels





plots <- grid.arrange(PF_plot + labs(title = NULL), PF_subset_plot_with_lines + labs(title = NULL) + theme(legend.position = "none"), CT_plot + labs(title = NULL), CT_subset_plot_with_lines + labs(title = NULL) + theme(legend.position = "none"), ncol = 2)



# Save the plot as a PNG file
ggsave("plots.pdf", plot = plots, width = 10, height = 5, dpi = 1500)


