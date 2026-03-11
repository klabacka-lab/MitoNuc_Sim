#!/bin/bash

start=$(date +%s)

source venv/bin/activate

for epi in T F; do
    for mut_profile in 1 2 3; do
        for preload_location in "mito" "nucl"; do
            echo "Preparing mut_profile=$mut_profile preload_location=$preload_location epistasis=$epi..."

            plot_dir="automatic_figures/2000"
            plot_filename="plot_mut${mut_profile}_preload[${preload_location}]_epi${epi}.png"
            plot_path="${plot_dir}/${plot_filename}"

            # Skip if figure already exists
            if [ -f "$plot_path" ]; then
                echo "Figure $plot_path already exists. Skipping simulations."
                continue
            fi

            echo "Running simulations..."

            rm -f sexual_cycles_to_escape.txt
            rm -f sexual_final_fitness.txt
            rm -f sexual_fitness_over_time.txt

            rm -f asexual_cycles_to_escape.txt
            rm -f asexual_final_fitness.txt
            rm -f asexual_fitness_over_time.txt

            for val in T F; do
                if [ "$val" = "F" ]; then
                    echo "Running sexual simulations..."
                else
                    echo "Running asexual simulations..."
                fi 

                for i in {1..100}; do
                    echo
                    echo
                    echo
                    echo "Running simulation $i..."

                    slim \
                    -d logging=T \
                    -d asexual="\"$val\"" \
                    -d mut_profile="$mut_profile" \
                    -d preload_location="\"$preload_location\"" \
                    -d epi="\"$epi\"" \
                    GrowthFitness.slim

                    python3 figure_maker.py --output "$plot_path"

                done
            done
        done
    done
done

end=$(date +%s)
echo "Elapsed time of simulation: $((end - start)) seconds"