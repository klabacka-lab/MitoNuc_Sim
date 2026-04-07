#!/bin/bash

# Check if the user provided a "MitoMutEffect" value as an argument
if [ -z "$1" ]; then
    echo "Error: Please provide a MitoMutEffect value as the first argument."
    exit 1
fi

# The value for MitoMutEffect from the user
mito_mut_effect="$1"

# Output CSV files
compensatory_csv="data_CompensatoryTest.csv"
peakfitness_csv="data_PeakFitness.csv"

# Create or clear the CSV files and add headers
echo "Replicate,Mode,Locus,SpecificModel,MitoMutEffect,FinalFitness" > "$compensatory_csv"
echo "Replicate,Mode,Locus,SpecificModel,MitoMutEffect,EndTime" > "$peakfitness_csv"

# Loop through all *_log.txt files
for file in *_log.txt; do
    # Extract Mode, Locus, and Experiment from the filename
    filename=$(basename "$file")
    IFS='_' read -r mode locus experiment _ <<< "$filename"

    # Create SpecificModel by joining Mode and Locus
    specific_model="${mode}_${locus}"

    # Initialize replicate counter
    replicate=1

    # Process based on experiment type
    if [[ "$experiment" == "CompensatoryTest" ]]; then
        # Extract Final Fitness values using sed
        sed -n 's/Final fitness: \([0-9.]\{1,\}\).*$/\1/p' "$file" | while read -r fitness; do
            # Append data to the CompensatoryTest CSV with MitoMutEffect value
            echo "$replicate,$mode,$locus,$specific_model,$mito_mut_effect,$fitness" >> "$compensatory_csv"
            replicate=$((replicate + 1))
        done
    elif [[ "$experiment" == "PeakFitness" ]]; then
        # Extract End Time values using sed
        sed -n 's/End Time: \([0-9.]\{1,\}\).*$/\1/p' "$file" | while read -r end_time; do
            # Append data to the PeakFitness CSV with MitoMutEffect value
            echo "$replicate,$mode,$locus,$specific_model,$mito_mut_effect,$end_time" >> "$peakfitness_csv"
            replicate=$((replicate + 1))
        done
    fi
done

echo "CSV files have been generated with MitoMutEffect: $mito_mut_effect."

