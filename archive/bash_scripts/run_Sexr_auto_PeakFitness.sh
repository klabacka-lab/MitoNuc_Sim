echo 'beginning to run {Sexr_auto_PeakFitness}'
 for i in {1..500}
do
slim Sexr_auto_PeakFitness.slim >> Sexr_auto_PeakFitness_log.txt
done
