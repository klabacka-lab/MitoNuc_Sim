echo 'beginning to run {Self_auto_PeakFitness}' 
 for i in {1..500}
do
slim Self_auto_PeakFitness.slim >> Self_auto_PeakFitness_log.txt
done
