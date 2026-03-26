# MitoNuc_Sim
Simulate evolutionary scenarios analogous to mitonuclear coevolution

Webpage for SLiM documentation: https://messerlab.org/slim/

# Setup

First, set up the Python virtual environment with the setup script:

```bash
./setup-venv.sh
source venv/bin/activate
```
# How to Set Up SLiM on the Supercomputer:

These instructions are explained, in section 2.2.2 (page 68), in the SLiM manual.

First, create a directory for software, or use one that has already been created.

```mkdir software
```
Enter the new directory.

```cd software
```
Download the source code.

``` wget https://github.com/MesserLab/SLiM/releases/download/v5.1/SLiM.zip
unzip SLiM.zip
```
You will need to use cmake in order to install SLiM.

Check to see if you already have it installed.
``` which cmake
```
If not, we’ll want to find cmake within the supercomputer.
``` module spider cmake
```
Then load it.
``` module load [cmake version spider found]
```
Next, we will follow the instructions as they appear in the manual.
```cd SLiM 
cd .. 
mkdir build 
cd build
```
Inside the build file, we will need to change cmake’s install prefix. 

```nano cmake
```
Inside cmake, select ^r then ^t
Select and enter the cmake_install.cmake file. At the top of the file, you are able to set the install prefix. 

Edit that section so it looks something like this:
# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "[path to your slim file]")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

Once that is complete and saved, you can finish installing.
 
```cmake ../SLiM 
make slim 
make install slim
```
[will give an error if install prefix was not changed]

Create path to SLiM

Include alias slim="/pathway/to/slim" within your .bashrc file. Make sure to replace /pathway/to/slim with the path in your system

Clone github
```git clone https://github.com/klabacka-lab/MitoNuc_Sim.git
```


# SIM 2

(All Sim 2 commands should be run from inside the Simulation_Preload directory)

## Main Simulation

GrowthFitness.slim runs a single simulation. It can be executed through the command line with the following syntax:

```bash
slim -d logging=T -d asexual=[T or F] -d mut_profile=[1, 2, or 3] -d preload_location=["mito" or "nucl"] -d epi=[T or F] -d data_file=[file_location] GrowthFitness.slim
```

The main simulation of interest should be run with `asexual` both on and off (the sim runs twice), `mut_profile` 1, `preload_location` set to "mito", and epistasis (`epi`) set to `T`. A file output location should be specified for each.

Suggested commands:

```bash
slim -d logging=T -d asexual=T -d mut_profile=1 -d preload_location=\"mito\" -d epi=T -d data_file=\"asex_result.txt\" GrowthFitness.slim
slim -d logging=T -d asexual=F -d mut_profile=1 -d preload_location=\"mito\" -d epi=T -d data_file=\"sex_result.txt\" GrowthFitness.slim
```

This simulation can be run multiple times with the same output location to append the results of several runs together. This can be done many times (5–10 each for sexual and asexual is a reasonable number for a manual replication check).

OPTIONALLY: If limited time or computing power prohibit the running of many simulations, pre-produced data from 800 runs each of the asexual and sexual simulations are included in the `Simulation_Preload` directory under the names `asexual_example_data.txt` and `sexual_example_data.txt` These can be fed into the figure-making and statistical testing scripts instead of files made by running the simulations directly.

## Plots/Figures

The files written by the above commands can be used to generate the figures in the paper when they are passed into the Python script `figure_maker.py` using the following syntax:

```bash
python figure_maker.py --sexual_data <data from sexual sim> --asexual_data <data from asexual sim> --output <desired output location>
```

Suggested command:

```bash
python figure_maker.py --sexual_data sex_result.txt --asexual_data asex_result.txt --output result_plot.png
```

This will produce an average fitness-over-time line plot alongside a boxplot for final fitnesses. These will be averaged across the different trials, and will show a shaded ±1 standard deviation around the average line. The boxplot will show the distribution of final fitnesses across all runs for each.

## Statistical Testing

Finally, feed the data to the statistical testing script:

```bash
python stat_analysis.py <input data file from asexual sim> <input data file from sexual sim> <output file location for a distribution visualization plot>
```

Suggested command:

```bash
python stat_analysis.py asex_result.txt sex_result.txt distro.png
```

This will output a written description of the results of running various statistical tests on the two distributions:

- Shapiro–Wilk test for normality
- Welch t-test for difference of means (results irrelevant if normality is rejected)
- Mann–Whitney U test for difference of central tendency (does not require normality)

The output file will be an extra PNG comparing the final fitness distributions as histograms, for intuitive visualization.
