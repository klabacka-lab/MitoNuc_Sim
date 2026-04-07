echo 'beginning to run {Sex_auto_PeakFitness}' 
 for i in {1..500}
do
slim Sex_auto_PeakFitness.slim >> Sex_auto_PeakFitness_log.txt
done
