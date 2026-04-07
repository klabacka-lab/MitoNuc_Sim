echo 'beginning to run {Asex_auto_CompensatoryTest}' 
 for i in {1..500}
do
slim Asex_auto_CompensatoryTest.slim >> Asex_auto_CompensatoryTest_log.txt
done
