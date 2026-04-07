echo 'beginning to run {Self_auto_CompensatoryTest}' 
 for i in {1..500}
do
slim Self_auto_CompensatoryTest.slim >> Self_auto_CompensatoryTest_log.txt
done
