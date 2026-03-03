#!/bin/bash

start=$(date +%s)

for val in T F; do
    if val == F; then
        echo "Running sexual simulations..."
        rm -f sexual_cycles_to_escape.txt
        rm -f sexual_final_fitness.txt
        rm -f sexual_fitness_over_time.txt
    else
        echo "Running asexual simulations..."
        rm -f asexual_cycles_to_escape.txt
        rm -f asexual_final_fitness.txt
        rm -f asexual_fitness_over_time.txt
    fi 
    for i in {1..100}; do
        echo "Running simulation $i..."
        slim -d asexual="\"$val\"" GrowthFitness.slim
        python3 figure_maker.py
    done
done

source venv/bin/activate
echo ""
echo ""
echo "-----Cycles to escape deleterious mutation: an analysis-----"
echo ""
python3 stat_analysis.py asexual_cycles_to_escape.txt sexual_cycles_to_escape.txt escape_cycles_distribution.png
echo ""
echo ""
echo "-----Final fitness: an analysis-----"
echo ""
python3 stat_analysis.py asexual_final_fitness.txt sexual_final_fitness.txt fitness_distribution.png

python3 figure_maker.py

echo "Final figure saved to fitness_over_time.png"

end=$(date +%s)
echo "Elapsed time of simulation: $((end - start)) seconds"

