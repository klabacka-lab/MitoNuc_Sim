echo 'beginning to run {Sexr_mito_adj_CompensatoryTest}'
 for i in {1..500}
do
slim Sexr_mito_adj_CompensatoryTest.slim >> Sexr_mito_adj_CompensatoryTest_log.txt
done
