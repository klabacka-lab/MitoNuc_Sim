# MitoNuc_Sim
Simulate evolutionary scenarios analogous to mitonuclear coevolution

Webpage for SLiM documentation: https://messerlab.org/slim/
(Messer Lab, Cornell University)

# Setup

### Clone github
```
git clone https://github.com/klabacka-lab/MitoNuc_Sim.git
```

## How to Set Up the Python Virtual Environment:

### Linux (recommended)
Run the setup script:

```bash
./setup-venv.sh
source venv/bin/activate
```
### MacOS (recommended)
```
python3 -m venv venv
```
or
```
pip install -r requirements.txt
```

### Windows (PowerShell - recommended)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Or for cmd:
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
```

## Installing SLiM
The github repo https://github.com/MesserLab/SLiM/blob/master/README.md has a readme with instructions for installing SLiM on a personal computer. The instructions are also explained in the SLiM manual (found on the Mercer Lab webpage) in section 2 (starting on page 60).

<details>

<summary>How to Set Up SLiM on the Supercomputer:</summary>

These instructions are explained in section 2.2.2 (page 68), in the SLiM manual. You can also download SLiM on the supercomputer using the github rather than source code: https://github.com/MesserLab/SLiM/blob/master/README.md

First, create a directory for software, or use one that has already been created.
```
mkdir software
```
Enter the new directory.
```
cd software
```
Download the source code.
``` 
wget https://github.com/MesserLab/SLiM/releases/download/v5.1/SLiM.zip
unzip SLiM.zip
```
You will need to use cmake in order to install SLiM.
Check to see if you already have it installed.
``` 
which cmake
```
If not, we’ll want to find cmake within the supercomputer.
``` 
module spider cmake
```
Then load it.
``` 
module load [cmake version spider found]
```
Next, we will follow the instructions as they appear in the manual.
```
cd SLiM 
cd .. 
mkdir build 
cd build
```
Inside the build file, we will need to change cmake’s install prefix. 

```
nano cmake
```
Inside cmake, select ^r then ^t
Select and enter the `cmake_install.cmake` file. At the top of the file, you are able to set the install prefix. 

Edit that section so it looks something like this:
```
#Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "[path to your slim file]")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")
```
Once that is complete and saved, you can finish installing.
 
```
cmake ../SLiM 
make slim 
make install slim
```
[will give an error if install prefix was not changed]

Create path to SLiM

Include ```alias slim="/pathway/to/slim"``` within your .bashrc file. Make sure to replace ```/pathway/to/slim``` with the path in your system
</details>

# SIM 1

## Supercomputer Setup

Create a folder for this project on the supercomputer

within that folder, add the scripts from the github directory:
```NoPreload_Multi_Batch.sh```
```NoPreload_Single_Batch.sh```
```NoPreload.slim```

Create an empty folder within your project folder named ```temp```

Add the script ```CombineTrials.sh``` into the temp folder from the github directory 

## Running a single trial

To run a single trial of a simulation 1, use the following syntax:

```bash
slim -d sex=[T or F] -d ben=[T or F] -d epi=[T or F] -d epiSt=[Epistasis Strength] -d recom=[Recombination Rate]  -d tagAmount=[Number of Mutation Tags] -d repID=[Trial Number] NoPreload.slim
```

## Running a batch of 100 trials

To run a batch of 100 trials of simulation 1, use the following syntax:
```bash
./NoPreload_Multi_Batch.sh [T or F] [T or F] [T or F] [Epistasis Strength] [Recombination Strength] [Number of Mutation Tags]
```

## Testing recombination rates

To test recombination rates in sexual populations, execute the previous batch command once per recombination rate (a total of seven times), using:
```bash
./NoPreload_Multi_Batch.sh T T T 100 <recomb> 20
```
Where `<recomb>` is one of:
0, 1.0e-07, 5.0e-6, 1.0e-06, 1.0e-05, 1.0e-04, 1.0e-03.

Or if running for just a single trial for testing recombination rate instead of a batch of 100, use the following command:
```bash
slim -d sex=T -d ben=T -d epi=T -d epiSt=100 -d recom=<recomb>  -d tagAmount=20 -d repID=1 NoPreload.slim
```
Where `<recomb>` is one of:
0, 1.0e-07, 5.0e-6, 1.0e-06, 1.0e-05, 1.0e-04, 1.0e-03.

## Testing epistasis strengths

To test epistasis strengths in sexual populations, execute the batch command once per epistasis strength (a total of six times), using:
```bash
./NoPreload_Multi_Batch.sh T T T <epi_strength> 5.0e-06 20
```
Where `<epi_strength>` is one of:
50, 100, 250, 500, 1000, 10000

Or if running for just a single trial for testing epistasis strength in sexual populations instead of a batch of 100, use the following command:
```bash
slim -d sex=T -d ben=T -d epi=T -d epiSt=<epi_strength> -d recom=5.0e-06  -d tagAmount=20 -d repID=1 NoPreload.slim
```
Where <epi_strength> is one of:
50, 100, 250, 500, 1000, 10000

To test epistasis strengths in asexual populations, execute the batch command once per epistasis rate (a total of six times), using:
```bash
./NoPreload_Multi_Batch.sh F T T <epi_strength> 0 20
```
Where <epi_strength> is one of:
50, 100, 250, 500, 1000, 10000

Or if running for just a single trial for testing epistasis strength in asexual populations instead of a batch of 100, use the following command:
```bash
slim -d sex=F -d ben=T -d epi=T -d epiSt=<epi_strength> -d recom=5.0e-06  -d tagAmount=20 -d repID=1 NoPreload.slim
```
Where <epi_strength> is one of:
50, 100, 250, 500, 1000, 10000

## Testing epistasis tags

To test epistasis tags in sexual populations, execute the batch command once per epistasis tag value (a total of nine times), using:
```bash
./NoPreload_Multi_Batch.sh T T T 100 5.0e-06 <epi_tag>
```
Where <epi_tag> is one of:
2, 5, 10, 15, 20, 25, 30, 50, 100

Or if running for just a single trial for testing epistasis tags in sexual populations instead of a batch of 100, use the following command:
```bash
slim -d sex=T -d ben=T -d epi=T -d epiSt=100 -d recom=5.0e-06  -d tagAmount=<epi_tag> -d repID=1 NoPreload.slim
```
Where <epi_tag> is one of:
2, 5, 10, 15, 20, 25, 30, 50, 100

To test epistasis tags in asexual populations, execute the batch command once per epistasis rate (a total of nine times), using:
```bash
./NoPreload_Multi_Batch.sh F T T 100 0 <epi_tag>
```
Where <epi_tag> is one of:
2, 5, 10, 15, 20, 25, 30, 50, 100

Or if running for just a single trial for testing epistasis tags in asexual populations instead of a batch of 100, use the following command:
```bash
slim -d sex=F -d ben=T -d epi=T -d epiSt=100 -d recom=5.0e-06  -d tagAmount=<epi_tag> -d repID=1 NoPreload.slim
```
Where <epi_tag> is one of:
2, 5, 10, 15, 20, 25, 30, 50, 100

## Testing absence of beneficial mutations

To test the effect of no beneficial mutations in sexual populations, execute the the following batch command:
```bash
./NoPreload_Multi_Batch.sh T F T 100 5.0e-06 20
```

Or if running for just a single trial for testing absence of benefifical mutations in sexual populations instead of a batch of 100, use the following command:
```bash
slim -d sex=T -d ben=F -d epi=T -d epiSt=100 -d recom=5.0e-06  -d tagAmount=20 -d repID=1 NoPreload.slim
```

To test the effect of no beneficial mutations in asexual populations, execute the the following batch command:
```bash
./NoPreload_Multi_Batch.sh F F T 100 0 20
```

Or if running for just a single trial for testing absence of benefifical mutations in asexual populations instead of a batch of 100, use the following command:
```bash
slim -d sex=F -d ben=F -d epi=T -d epiSt=100 -d recom=0  -d tagAmount=20 -d repID=1 NoPreload.slim
```

## Testing no epistasis

To test the effect of no epistasis in sexual populations, execute the the following batch command:
```bash
./NoPreload_Multi_Batch.sh T T F 100 5.0e-06 20
```

Or if running for just a single trial for testing absence of epistasis in sexual populations instead of a batch of 100, use the following command:
```bash
slim -d sex=T -d ben=T -d epi=F -d epiSt=100 -d recom=5.0e-06  -d tagAmount=20 -d repID=1 NoPreload.slim
```

To test the effect of no epistasis in asexual populations, execute the the following batch command:
```bash
./NoPreload_Multi_Batch.sh F T F 100 0 20
```

Or if running for just a single trial for testing absence of epistasis in asexual populations instead of a batch of 100, use the following command:
```bash
slim -d sex=F -d ben=T -d epi=F -d epiSt=100 -d recom=0  -d tagAmount=20 -d repID=1 NoPreload.slim
```

## Running analysis

After running these, run the following command to organize the files in the temp directory after all trials are finished running:
```bash
./temp/CombineTrials.sh
```

Files created will be named according to the following template:
[sex or asex]_[ben or noben]_[epi or noepi]_[Epistasis Strength]_[Recombination Rate]_[Number of Tags].csv

"sex_ben_epi_1_5.0e-06_20.csv" is an example with the following parameters:

sexual reproduction, beneficial mutations, epistasis on, epistasis strength = 1, recombination rate = 5.0e-06, number of tags = 20

Some files with recombination values of 1.0e-03 and 1.0e-04 may be titled with 0.001 and 0.0001 respectfully. To ensure compatability with statistics file, ensure these files are named with recombination value in scientific notation following 1.0e-03 format

Download and move all combined csv data files from the temp directory on the supercomputer to the NoPreload_Data folder in the github directory:

To run statistical analysis and generate noPreload_results.csv, which contains the resulting p-values, run the following command:
```
R run_statistics.R
```
For visualization code, ensure you are located in the Simulation_NoPreload directory by running:
```bash
cd ./Simulation_NoPreload
```

To generate figures comparing trials, use the following syntax:
```bash
python ./visualMaker.py <path/to/csv/1> <path/to/csv/2>
```

To see an example of this, these are the commands we ran to generate the figures we ended up using:

```bash
python ./visualMaker.py ./NoPreload_Data/sex_ben_epi_100_5.0e-06_2.csv ./NoPreload_Data/asex_ben_epi_100_0_2.csv
python ./visualMaker.py ./NoPreload_Data/sex_ben_epi_100_5.0e-06_20.csv ./NoPreload_Data/asex_ben_epi_100_0_20.csv
python ./visualMaker.py ./NoPreload_Data/sex_ben_epi_100_5.0e-06_100.csv ./NoPreload_Data/asex_ben_epi_100_0_100.csv
python ./visualMaker.py ./NoPreload_Data/sex_ben_epi_50_5.0e-06_20.csv ./NoPreload_Data/asex_ben_epi_50_0_20.csv
python ./visualMaker.py ./NoPreload_Data/sex_ben_epi_10000_5.0e-06_20.csv ./NoPreload_Data/asex_ben_epi_10000_0_20.csv
```

We utilized this code to generate a 3x2 including the data from the 5 examples above:
```bash
python ./visualGrid.py 
```

# SIM 2

This simulation starts a population at a low initial fitness to compare the ability of sexually and asexually reproducing populations to recover from that low fitness.

(All Sim 2 commands should be run from inside the Simulation_Preload directory)

```bash
cd Simulation_Preload
```

## Quickstart/TL;DR
The following bash blocks allow the entire proess to be run in one step

For a quick start with preloaded data, execute the following:
```bash
python make_figure_3.py
python figure_3_statistics.py
```

For a quick start that actually runs the simulations, excecute the following:
```bash
./run_fig_3.sh fig_3_test 10
python make_figure_3.py --folder fig_3_test
python figure_3_statistics.py --folder fig_3_test
```

In either case, the output results are found in result_plot.png (fitness over time graph with final fitness distubution boxplots) and the terminal output

If not using the quickstart blocks, perform the following discrete steps:

## Main Simulation
GrowthFitness.slim runs a single simulation. It can be executed through the command line with the following syntax:

```bash
slim -d logging=T -d asexual=[T or F] -d mut_profile=[1, 2, or 3] -d preload_location=["mito" or "nucl"] -d epi=[T or F] -d data_file=[file_location] -d num_tags=[number of tags] -d epi_rate=[epistatic constant] GrowthFitness.slim
```

The main simulation of interest should be run with `asexual` both on and off (the sim runs twice), `mut_profile` 1, `preload_location` set to "mito", and epistasis (`epi`) set to `T`. A file output location should be specified for each. 5 different choices for `num_tags` and `epi_rate` are needed to reproduce our exact result, so running simulations manually is not reccomended. 

For convenience, the necessary script execution lines are wrapped in a for loop in the script `run_fig_3.sh`. It takes command line arguments with a data storage directory and the number of times to run both the sexual and asexual simulations. It can be run for 10 simulations like so:

```bash
./run_fig_3.sh [data dir] 10
```

OPTIONALLY: If limited time or computing power prohibit the running of many simulations, pre-produced data from 100 runs each of the asexual and sexual simulations are included in the `cached_data/fig_3` directory. This is the default for the figure-making and statistical testing scripts when no file locations are passed in. This may be the only way to obtain our exact results, as they require a high sample size to gain statistical power. This can be seen in the quickstartinstructions

## Plots/Figures

The files written by the above commands can be used to generate the figures in the paper when they are passed into the Python script `figure_maker.py` using the following syntax:

```bash
python make_figure_3.py --folder [data dir]
```

This will produce a set of boxplots comparing the effects of differing numbers of epistatic tags (one row) and differing epistatic strength constants (the other). It will be saved as `fig_3.py`

## Statistical Testing

Finally, feed the data to the statistical testing script:

```bash
python figure_3_statistics.py --folder [data dir]
```

This will output a `fig3_statistics.csv` with the following column headers:

`test, p_value, significant, direction`

Where the `test` column describes the configuration being tested, the `p_value` column gives the resulting p-value for the test, the `significant` column gives a boolean value for whether the result is statistically significant, and the `direction` column gives the direction of the difference (which group had higher final fitness on average).
