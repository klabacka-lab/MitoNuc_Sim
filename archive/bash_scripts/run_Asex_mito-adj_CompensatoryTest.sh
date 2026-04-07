echo 'beginning to run {Asex_mito_adj_CompensatoryTest}' 
 for i in {1..500}
do
slim Asex_mito_adj_CompensatoryTest.slim >> Asex_mito_adj_CompensatoryTest_log.txt
done
