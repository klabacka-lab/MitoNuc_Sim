SEX=$1
BEN=$2
EPI=$3
STRENGTH=$4
RECOM=$5
echo "Running combination: sex=$SEX ben=$BEN epi=$EPI strength=$STRENGTH"

# Run 100 replicates
for i in {1..120}; do
    echo "Replicate $i"
    sbatch sbatchEfficient.sh $SEX $BEN $EPI $STRENGTH $RECOM 
done
