SIM 2

#Setup

(All commands should be executed in the Simulation_Preload directory)

First, set up the Python virtual environment with the setup script:

`./setup-venv.sh`
`source venv/bin/activate`

#Main Simulation

GrowthFitness.slim runs a single simulation. It can be excecuted through the command line with the syntax:

`slim -d logging=T -d asexual=[T or F] -d mut_profile=[1, 2, or 3] -d preload_location=["mito" or "nucl"] -d epi=[T or F] -d data_file=[file_location] GrowthFitness.slim`

The main simulation of interest should be run with asexual both on and off (sim runs twice), mut_profile 1, preload_location "mito", and epistasis (epi)  as T. A file output location should be specified for each.

Suggested commands:
`slim -d logging=T -d asexual=T -d mut_profile=1 -d preload_location="mito" -d epi=T -d data_file=asex_result.txt GrowthFitness.slim`
`slim -d logging=T -d asexual=F -d mut_profile=1 -d preload_location="mito" -d epi=T -d data_file=sex_result.txt GrowthFitness.slim`


This simulation can be run multiple times with the same output location to append the results of several runs together. This can be done many times (5-10 each for sexual and asexual is a reasonable number for a manual replication check). 

#Plots/Figures

The files written by the above commands can be used to generate the figures in the paper when the are passed into the python script "figure_maker.py" using the following syntax.

`python figure_maker.py --sexual_data [data from asexual sim] --asexual_data [data from asexual sim] --output [desired output location]`

Suggested command:

`python figure_maker.py --sexual_data sex_result --asexual_data asex_result.txt --output result_plot.png`

This will produce a an average fitness-over-time line plot alongside a boxplot for final fitnesses. These will be averaged across the different trials, and will show a shaded +- 1 standard deviation around the average line. The boxplot will show the distribution of final fitnesses across all runs for each.

#Statistical Testing

Finally, feed the data to the statistical testing script:

Syntax:
`python stat_analysis.py [input data file from asexual sim] [input data file from sexual sim] [output file location for a distribution visualization plot]`

Suggested command:
`python stat_analysis.py asex_result.txt sex_result.txt distro.py`

This will output a written description of the results of running various statistcal tests on the two distributions:

Shapiro-Wilk test for normality
Welch T-test for difference of means (results irrelevant if normality is rejected)
Mann-Whitney U-test for difference of central tendency (does not require normality)

The output file will be an extra png comparing the final fitness distributions as histograms, for intitive visualization.




