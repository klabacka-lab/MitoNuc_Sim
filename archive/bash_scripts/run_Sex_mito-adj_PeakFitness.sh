echo 'beginning to run {Sex_mito_adj_PeakFitness}' 
 for i in {1..500}
do
slim Sex_mito_adj_PeakFitness.slim >> Sex_mito_adj_PeakFitness_log.txt
done
