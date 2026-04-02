#!/bin/bash

start=$(date +%s)

source venv/bin/activate

tags=(2 20 100 20 20)
epis=(100 100 100 50 1000)

plot_dir="automatic_figures/fig_3"

for idx in "${!tags[@]}"; do
    num_tags="${tags[$idx]}"
    epi_const="${epis[$idx]}"

    run_id="tags${num_tags}_epi${epi_const}"

    echo "Preparing $run_id..."

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

        data_file="${plot_dir}/${prefix}_${run_id}_data.txt"

        rm -f "$data_file"

        for i in {1..3}; do
            echo
            echo "Running simulation $i..."

            slim \
                -d logging=T \
                -d asexual="\"$val\"" \
                -d mut_profile=1 \
                -d preload_location="\"mito\"" \
                -d epi=T \
                -d data_file="\"$data_file\"" \
                -d num_tags="$num_tags" \
                -d epi_rate="$epi_const" \
                GrowthFitness.slim

            python3 figure_maker.py \
                --sexual_data "${plot_dir}/sexual_${run_id}_data.txt" \
                --asexual_data "${plot_dir}/asexual_${run_id}_data.txt" \
                --output "$plot_path"
        done
    done
done

end=$(date +%s)
echo "Elapsed time of simulation: $((end - start)) seconds"