#!/usr/bin/env bash

if [[ $# -gt 1 ]]; then
    exit 1
fi

runs="${1:-10}"

for (( run=1; run<=runs; run++ )); do
    slim -d logging=T -d asexual=T -d mut_profile=1 -d preload_location=\"mito\" -d epi=T -d data_file=\"asex_result.txt\" GrowthFitness.slim
    slim -d logging=T -d asexual=F -d mut_profile=1 -d preload_location=\"mito\" -d epi=T -d data_file=\"sex_result.txt\" GrowthFitness.slim
done
