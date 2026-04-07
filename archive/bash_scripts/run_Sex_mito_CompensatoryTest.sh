echo 'beginning to run {Sex_mito_CompensatoryTest}' 
 for i in {1..500}
do
slim Sex_mito_CompensatoryTest.slim >> Sex_mito_CompensatoryTest_log.txt
done
