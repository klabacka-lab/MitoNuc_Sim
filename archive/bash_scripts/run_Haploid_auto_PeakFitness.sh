echo 'beginning to run {Haploid_auto_PeakFitness}' 
 for i in {1..500}
do
slim Haploid_auto_PeakFitness.slim >> Haploid_auto_PeakFitness_log.txt
done
