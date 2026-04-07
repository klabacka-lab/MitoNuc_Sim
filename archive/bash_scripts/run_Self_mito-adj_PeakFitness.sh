echo 'beginning to run {Self_mito_adj_PeakFitness}' 
 for i in {1..500}
do
slim Self_mito_adj_PeakFitness.slim >> Self_mito_adj_PeakFitness_log.txt
done
