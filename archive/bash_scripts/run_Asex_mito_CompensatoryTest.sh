echo 'beginning to run {Asex_mito_CompensatoryTest}' 
 for i in {1..500}
do
slim Asex_mito_CompensatoryTest.slim >> Asex_mito_CompensatoryTest_log.txt
done
