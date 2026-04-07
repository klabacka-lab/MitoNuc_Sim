echo 'beginning to run {Asex_auto_PeakFitness}' 
 for i in {1..500}
do
slim Asex_auto_PeakFitness.slim >> Asex_auto_PeakFitness_log.txt
done
