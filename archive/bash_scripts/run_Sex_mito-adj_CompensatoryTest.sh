echo 'beginning to run {Sex_mito_adj_CompensatoryTest}' 
 for i in {1..500}
do
slim Sex_mito_adj_CompensatoryTest.slim >> Sex_mito_adj_CompensatoryTest_log.txt
done
