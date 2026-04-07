echo 'beginning to run {Herm_auto_PeakFitness}' 
 for i in {1..500}
do
slim Herm_auto_PeakFitness.slim >> Herm_auto_PeakFitness_log.txt
done
