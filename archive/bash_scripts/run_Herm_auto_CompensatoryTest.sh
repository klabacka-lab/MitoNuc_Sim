echo 'beginning to run {Herm_auto_CompensatoryTest}' 
 for i in {1..500}
do
slim Herm_auto_CompensatoryTest.slim >> Herm_auto_CompensatoryTest_log.txt
done
