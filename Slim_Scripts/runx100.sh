#!/bin/bash

start=$(date +%s)

source venv/bin/activate

for epi in T F; do
    for mut_profile in 1 2 3; do
        for preload_location in "mito" "nucl"; do

            run_id="mut${mut_profile}_preload_${preload_location}_epi${epi}"

            echo "Preparing $run_id..."

            mkdir -p "$data_dir"

            plot_dir="automatic_figures/2000"
            plot_filename="plot_${run_id}.png"
            plot_path="${plot_dir}/${plot_filename}"

            # Skip if figure already exists
            if [ -f "$plot_path" ]; then
                echo "Figure $plot_path already exists. Skipping simulations."
                continue
            fi

            echo "Running simulations..."

            for val in T F; do

                if [ "$val" = "F" ]; then
                    echo "Running sexual simulations..."
                    prefix="sexual"
                else
                    echo "Running asexual simulations..."
                    prefix="asexual"
                fi 

                data_file="${prefix}_${run_id}_data.txt"



                for i in {1..100}; do
                    echo
                    echo "Running simulation $i..."

                    slim \
                    -d logging=T \
                    -d asexual="\"$val\"" \
                    -d mut_profile="$mut_profile" \
                    -d preload_location="\"$preload_location\"" \
                    -d epi="\"$epi\"" \
                    -d data_file="\"$data_file\"" \
                    GrowthFitness.slim

                    python3 figure_maker.py \
                        --input "$data_dir" \
                        --output "$plot_path"

                done
            done
        done
    done
done

end=$(date +%s)
echo "Elapsed time of simulation: $((end - start)) seconds"