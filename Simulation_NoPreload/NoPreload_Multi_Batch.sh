SEX=$1
BEN=$2
EPI=$3
STRENGTH=$4
RECOM=$5
TAGS=$6

echo "Running combination: sex=$SEX ben=$BEN epi=$EPI strength=$STRENGTH tag=$TAGS"

# Run 100 replicates
for i in {1..100}; do
    echo "Replicate $i"
    sbatch sbatchEfficient.sh $SEX $BEN $EPI $STRENGTH $RECOM $TAGS $i
done