echo 'beginning to run {Sexr_mito_CompensatoryTest}'
 for i in {1..500}
do
slim Sexr_mito_CompensatoryTest.slim >> Sexr_mito_CompensatoryTest_log.txt
done
