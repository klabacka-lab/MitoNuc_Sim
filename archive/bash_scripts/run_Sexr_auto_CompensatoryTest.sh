echo 'beginning to run {Sexr_auto_CompensatoryTest}'
 for i in {1..500}
do
slim Sexr_auto_CompensatoryTest.slim >> Sexr_auto_CompensatoryTest_log.txt
done
