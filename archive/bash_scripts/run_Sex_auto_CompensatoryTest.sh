echo 'beginning to run {Sex_auto_CompensatoryTest}' 
 for i in {1..500}
do
slim Sex_auto_CompensatoryTest.slim >> Sex_auto_CompensatoryTest_log.txt
done
