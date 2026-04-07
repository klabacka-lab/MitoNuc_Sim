echo 'beginning to run {Self_mito_CompensatoryTest}' 
 for i in {1..500}
do
slim Self_mito_CompensatoryTest.slim >> Self_mito_CompensatoryTest_log.txt
done
