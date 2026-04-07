echo 'beginning to run {Sex_mito_PeakFitness}' 
 for i in {1..500}
do
slim Sex_mito_PeakFitness.slim >> Sex_mito_PeakFitness_log.txt
done
