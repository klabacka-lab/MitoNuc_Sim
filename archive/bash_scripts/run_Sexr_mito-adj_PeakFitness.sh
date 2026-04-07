echo 'beginning to run {Sexr_mito_adj_PeakFitness}'
 for i in {1..500}
do
slim Sexr_mito_adj_PeakFitness.slim >> Sexr_mito_adj_PeakFitness_log.txt
done
