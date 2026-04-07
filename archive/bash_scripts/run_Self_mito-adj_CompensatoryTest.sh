echo 'beginning to run {Self_mito_adj_CompensatoryTest}' 
 for i in {1..500}
do
slim Self_mito_adj_CompensatoryTest.slim >> Self_mito_adj_CompensatoryTest_log.txt
done
