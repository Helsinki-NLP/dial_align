#! /bin/bash -l

#SBATCH -J eflomallevpriors
#SBATCH -o log_eflomallevpriors.%j.out
#SBATCH -e log_eflomallevpriors.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 24:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-efmaral

set -e
DATADIR=../../data

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	python3 makelevpriors.py "../leven/$PROJECT/*.fwd" $PROJECT.priors
	mkdir -p $PROJECT

	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		align_eflomal.py -s $DATADIR/$PROJECT/$FID".orig" -t $DATADIR/$PROJECT/$FID".norm" -f $PROJECT/$FID".fwd" -r $PROJECT/$FID".rev" --priors $PROJECT.priors
		atools -c grow-diag-final-and -i $PROJECT/$FID".fwd" -j $PROJECT/$FID".rev" > $PROJECT/$FID".sym"
	done
done
