echo 'beginning to run {Haploid_mito_adj_CompensatoryTest}' 
 for i in {1..500}
do
slim Haploid_mito_adj_CompensatoryTest.slim >> Haploid_mito_adj_CompensatoryTest_log.txt
done
