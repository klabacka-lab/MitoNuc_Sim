echo 'beginning to run {Herm_mito_PeakFitness}' 
 for i in {1..500}
do
slim Herm_mito_PeakFitness.slim >> Herm_mito_PeakFitness_log.txt
done
