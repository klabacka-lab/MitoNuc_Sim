echo 'beginning to run {Herm_mito_adj_PeakFitness}' 
 for i in {1..500}
do
slim Herm_mito_adj_PeakFitness.slim >> Herm_mito_adj_PeakFitness_log.txt
done
