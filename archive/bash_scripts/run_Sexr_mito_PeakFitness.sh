echo 'beginning to run {Sexr_mito_PeakFitness}'
 for i in {1..500}
do
slim Sexr_mito_PeakFitness.slim >> Sexr_mito_PeakFitness_log.txt
done
