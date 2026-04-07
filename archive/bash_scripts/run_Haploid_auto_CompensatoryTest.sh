echo 'beginning to run {Haploid_auto_CompensatoryTest}' 
 for i in {1..500}
do
slim Haploid_auto_CompensatoryTest.slim >> Haploid_auto_CompensatoryTest_log.txt
done
