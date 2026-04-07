echo 'beginning to run {Asex_mito_PeakFitness}' 
 for i in {1..500}
do
slim Asex_mito_PeakFitness.slim >> Asex_mito_PeakFitness_log.txt
done
