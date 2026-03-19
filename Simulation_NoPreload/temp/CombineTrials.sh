#!/bin/bash

cd temp || { echo "temp directory not found"; exit 1; }

for base in $(ls *_Trial*.csv | sed -E 's/_Trial[0-9]+\.csv//' | sort | uniq)
do
    echo "Combining trials for $base..."

    cat $(ls ${base}_Trial*.csv | sort -V) > ${base}.csv

    rm ${base}_Trial*.csv

    echo "Created ${base}.csv and deleted trial files."
done

echo "All trials combined successfully."
