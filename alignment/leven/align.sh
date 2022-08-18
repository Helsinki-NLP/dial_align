#! /bin/bash -l

#SBATCH -J leven
#SBATCH -o log_leven.%j.out
#SBATCH -e log_leven.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 2:00:00

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
		python ../levenshtein_align.py -method edlib -src $DATADIR/$PROJECT/$FID".orig" -tgt $DATADIR/$PROJECT/$FID".norm" -fwd $PROJECT/$FID".fwd" -rev $PROJECT/$FID".rev"
		python ../add_adjacent_identicals.py $DATADIR/$PROJECT/$FID".orig" $DATADIR/$PROJECT/$FID".norm" $PROJECT/$FID".fwd" $PROJECT/$FID".fwd+aai"
	done
done

deactivate

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-efmaral

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  SYM $FID"
		atools -c grow-diag-final-and -i $PROJECT/$FID".fwd" -j $PROJECT/$FID".rev" > $PROJECT/$FID".sym"
	done
done
