echo 'beginning to run {Herm_mito_adj_CompensatoryTest}' 
 for i in {1..500}
do
slim Herm_mito_adj_CompensatoryTest.slim >> Herm_mito_adj_CompensatoryTest_log.txt
done
