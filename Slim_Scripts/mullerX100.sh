#!/bin/bash

start=$(date +%s)

rm -f sex_ben_epi.csv
rm -f asex_ben_epi.csv
rm -f sex_ben_noepi.csv
rm -f asex_ben_noepi.csv
rm -f sex_noben_epi.csv
rm -f asex_noben_epi.csv
rm -f sex_noben_noepi.csv
rm -f asex_noben_noepi.csv




for sex in T F; do
    for ben in T F; do
        for epi in T F; do
            for i in {1..100}; do
                echo "Running simulation $i..."
                slim -d sex="\"$sex\"" ben="\"$ben\"" epi="\"$epi\"" FitnessSexStates.slim
            done
        done
    done
done

echo "Elapsed time of simulation: $((end - start)) seconds"
