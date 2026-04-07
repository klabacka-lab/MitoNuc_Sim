library(ggplot2)

setwd('/Users/r_klabacka/OneDrive - Utah Tech University/KLab/Research/MitoNuc_Sim/RunningFiles')

## PEAK FITNESS DATA

# Obtain the peak fitness data
dat_PF_all <- read.csv('PeakFitness_data.csv')

# reduce the dataset for just sex and asex modes of reproduction
dat_PF <- dat_PF_all[dat_PF_all$Mode %in% c("Sex", "Asex"), ]
# get dataset with only mito
dat_PF_Mt <- dat_PF[dat_PF$Locus %in% c("mito"), ]
# create a dataset for the unadjusted mito data
dat_PF_MtAut <- dat_PF[dat_PF$Locus %in% c("mito", "auto"), ]
# create a dataset for the adjusted mito data
dat_PF_MtadjAut <- dat_PF[dat_PF$Locus %in% c("mito-adj", "auto"), ]

# test for a difference in time to reach peak fitness between sex and asex
PF_mito = lm(data = dat_PF_Mt, EndTime~Mode)


plot_PF_Mt <- ggplot(dat_PF_Mt, aes(x = Mode, y = EndTime, fill = Mode)) +
  geom_boxplot() +
  scale_fill_manual(values = c("Asex" = "#F0A6CA", "Sex" = "lightgray")) +  # Custom fill colors
  labs(x = NULL, y = "Time to reach peak fitness") +  # Remove x-axis label and rename y-axis
  theme_classic() +
  theme(
    legend.position = "none",        # Remove the legend
    axis.title.y = element_text(size = 1.5 * 11),  # Increase y-axis title font size by 50%
    axis.text = element_text(size = 1.5 * 11),     # Increase axis text font size by 50%
    axis.title.x = element_text(size = 1.5 * 11),  # Increase x-axis title font size (though x-axis title is removed)
    plot.title = element_text(size = 1.5 * 14)     # Increase plot title font size by 50%, if there's a title
  )

ggsave("Figures/PF_Mt.png", plot = plot_PF_Mt, width = 6, height = 8, dpi = 300)


# test for an interaction between mode (sex/asex) and locus (mito/auto)
PF_interaction1 = lm(data = dat_PF_MtadjAut, EndTime~Mode*Locus)

ggplot(dat_PF_all, aes(x = interaction(Mode, Locus), y = EndTime)) +
  geom_boxplot() +
  labs(x = "Mode and Locus Interaction", y = "End Time") +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# test for an interaction between mode (sex/asex) and locus (mito/auto) where the mutation rate doesn't differ between mito and auto
PF_interaction2 = lm(data = dat_PF_MtadjAut, EndTime~Mode*Locus)

ggplot(dat_PF_MtadjAut, aes(x = interaction(Mode, Locus), y = EndTime)) +
  geom_boxplot() +
  labs(x = "Mode and Locus Interaction", y = "End Time") +
  theme_classic()

# COMPENSATORY TEST DATA

dat_CT_all <- read.csv('CompensatoryTest_data.csv')
dat_CT <- dat_CT_all[dat_CT_all$Mode %in% c("Sex", "Asex"), ]
dat_CT_Mt <- dat_CT[dat_CT$Locus %in% c("mito"), ]

plot_CT_Mt <- ggplot(dat_CT_Mt, aes(x = Mode, y = FinalFitness, fill = Mode)) +
  geom_boxplot() +
  scale_fill_manual(values = c("Asex" = "#F0A6CA", "Sex" = "lightgray")) +  # Custom fill colors
  labs(x = NULL, y = "Final fitness") +  # Remove x-axis label and rename y-axis
  theme_classic() +
  theme(
    legend.position = "none",        # Remove the legend
    axis.title.y = element_text(size = 1.5 * 11),  # Increase y-axis title font size by 50%
    axis.text = element_text(size = 1.5 * 11),     # Increase axis text font size by 50%
    axis.title.x = element_text(size = 1.5 * 11),  # Increase x-axis title font size (though x-axis title is removed)
    plot.title = element_text(size = 1.5 * 14)     # Increase plot title font size by 50%, if there's a title
  )

ggsave("Figures/CT_Mt.png", plot = plot_CT_Mt, width = 6, height = 8, dpi = 300)

dat_CT_MtAut <- dat_CT[dat_CT$Locus %in% c("mito", "auto"), ]
dat_CT_MtadjAut <- dat_CT[dat_CT$Locus %in% c("mito-adj", "auto"), ]

CT_interaction1 = lm(data = dat_CT_MtAut, FinalFitness~Mode*Locus)
CT_interaction2 = lm(data = dat_CT_MtAut, FinalFitness~Mode*Locus)

ggplot(dat_CT_MtAut, aes(x = interaction(Mode, Locus), y = FinalFitness)) +
  geom_boxplot() +
  labs(x = "Mode and Locus Interaction", y = "FinalFitness") +
  theme_classic()


ggplot(dat_CT_MtadjAut, aes(x = interaction(Mode, Locus), y = FinalFitness)) +
  geom_boxplot() +
  labs(x = "Mode and Locus Interaction", y = "FinalFitness") +
  theme_classic()




ggplot(data = CT_interaction, aes(x = Mode, y = FinalFitness, fill=Mode)) + geom_boxplot(alpha = 0.5) + scale_fill_manual(values = c("#A9DBB8", "#7CA5B8", "#38369A", "#2139ed", "black")) + theme_classic()

results = lm(data = mito_PF, FinalFitness~relevel(factor(Mode), ref = "Asex"))

summary(results)

ggplot(data = mito_PF, aes(x = Mode, y = FinalFitness, fill=Mode)) + geom_violin(alpha = 0.5) + geom_jitter(width = .1) + scale_fill_manual(values = c("#A9DBB8", "#7CA5B8", "#38369A", "#2139ed", "black")) + theme_classic()
ggplot(data = mito_PF, aes(x = Mode, y = FinalFitness, fill=Mode)) + geom_boxplot(alpha = 0.5) + scale_fill_manual(values = c("#A9DBB8", "#7CA5B8", "#38369A", "#2139ed", "black")) + theme_classic()
mito_PF <- dat[dat$Locus == "mito", ]
