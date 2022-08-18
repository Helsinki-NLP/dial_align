#! /bin/bash -l

#SBATCH -J leven_pmi
#SBATCH -o log_leven_pmi.%j.out
#SBATCH -e log_leven_pmi.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 4:00:00

DATADIR=../../data

module load python-data
source ../../pyenv/bin/activate

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		python3 ../compute_pmi.py "../leven/$PROJECT/$FID.fwd" $PROJECT/$FID.costs
		python ../levenshtein_align.py -method weighted -src $DATADIR/$PROJECT/$FID".orig" -tgt $DATADIR/$PROJECT/$FID".norm" -fwd $PROJECT/$FID".fwd" -costs $PROJECT/$FID.costs
		python ../add_adjacent_identicals.py $DATADIR/$PROJECT/$FID".orig" $DATADIR/$PROJECT/$FID".norm" $PROJECT/$FID".fwd" $PROJECT/$FID".fwd+aai"
	done
done
deactivate
