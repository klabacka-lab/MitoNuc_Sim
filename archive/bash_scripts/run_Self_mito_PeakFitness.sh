echo 'beginning to run {Self_mito_PeakFitness}' 
 for i in {1..500}
do
slim Self_mito_PeakFitness.slim >> Self_mito_PeakFitness_log.txt
done
