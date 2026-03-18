SIM 2

GrowthFitness.slim runs a single simulation. It can be excecuted through the command line with the syntax:

slim -d logging=T -d asexual=[T or F] -d mut_profile=[1, 2, or 3] -d preload_location=["mito" or "nucl"] -d epi=[T or F] -d data_file=[file_location] GrowthFitness.slim

The main simulation of interest should be run with asexual both on and off (run twice), mut_profile 1, preload_location "mito", and epistais on (epi) (T). A file output location should be specified for each.

This simulation can be run miltiple times with the same output location to append the results of several runs together. This can be done several times (5-10 each for sexual and asexual is a resonable number for a manual replication check). 

The files written by the above command can be used to generate the figures in the paper. They can be passed into the python script "figure_maker.py" after activating the venv.

source venv/bin/activate
python figure_maker.py --sexual_data [data from asexual sim] --asexual_data [data from asexual sim] --output [desired output location]

This will produce a an average fitness-over-time line plot alongside a boxplot for final fitnesses. These will be averaged across however many runs were performed for each, and will show a +- 1 standard deviation shaded area around the average line. The boxplot will show the distribution of final fitnesses across all runs for each.



