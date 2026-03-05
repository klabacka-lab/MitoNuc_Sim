#!/bin/bash

#SBATCH --time=24:00:00 #walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --mem-per-cpu=1024M   # memory per CPU core
#SBATCH --mail-user=jac2002@byu.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL



# Set the max number of threads to use for programs using OpenMP. Should be <= ppn. Does nothing if the program doesn't use OpenMP.
export OMP_NUM_THREADS=$SLURM_CPUS_ON_NODE

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE


SEX=$1
BEN=$2
EPI=$3
STRENGTH=$4

echo "Running combination: sex=$SEX ben=$BEN epi=$EPI strength=$STRENGTH"

# Run 100 replicates
for i in {1..100}; do
    echo "Replicate $i"
    /home/jac2002/.local/bin/slim \
        -d sex=$SEX \
        -d ben=$BEN \
        -d epi=$EPI \
        -d epiSt=$STRENGTH \
        FitnessSexStates.slim
done
