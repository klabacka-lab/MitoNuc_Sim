echo 'beginning to run {Asex_mito_adj_PeakFitness}' 
 for i in {1..500}
do
slim Asex_mito_adj_PeakFitness.slim >> Asex_mito_adj_PeakFitness_log.txt
done
