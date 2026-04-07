echo 'beginning to run {Haploid_mito_CompensatoryTest}' 
 for i in {1..500}
do
slim Haploid_mito_CompensatoryTest.slim >> Haploid_mito_CompensatoryTest_log.txt
done
