#!/bin/bash

start=$(date +%s)

source venv/bin/activate


for mut_profile in 1 2 3; do
    for preload_location in "mito" "nuc"; do
        echo "Running simulations with mut_profile=$mut_profile and preload_location=$preload_location"

        rm -f sexual_cycles_to_escape.txt
        rm -f sexual_final_fitness.txt
        rm -f sexual_fitness_over_time.txt

        rm -f asexual_cycles_to_escape.txt
        rm -f asexual_final_fitness.txt
        rm -f asexual_fitness_over_time.txt

        plot_dir="automatic_figures"

        plot_filename = "plot_mut${mut_profile}_preload[${preload_location}].png"

        for val in T F; do
            if [ "$val" = "F" ]; then
                echo "Running sexual simulations..."
            else
                echo "Running asexual simulations..."
            fi 
            for i in {1..100}; do
                echo "\n\n\n"
                echo "Running simulation $i..."
                slim -d asexual="\"$val\"" -d mut_profile="$mut_profile" -d preload_location="\"$preload_location\"" GrowthFitness.slim
                python3 figure_maker.py ${plot_dir}/${plot_filename}

            done
        done

    done
done

end=$(date +%s)
echo "Elapsed time of simulation: $((end - start)) seconds"



