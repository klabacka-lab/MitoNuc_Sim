echo 'beginning to run {Haploid_mito_PeakFitness}' 
 for i in {1..500}
do
slim Haploid_mito_PeakFitness.slim >> Haploid_mito_PeakFitness_log.txt
done
