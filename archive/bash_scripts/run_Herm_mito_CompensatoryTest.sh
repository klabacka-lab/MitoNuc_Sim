echo 'beginning to run {Herm_mito_CompensatoryTest}' 
 for i in {1..500}
do
slim Herm_mito_CompensatoryTest.slim >> Herm_mito_CompensatoryTest_log.txt
done
