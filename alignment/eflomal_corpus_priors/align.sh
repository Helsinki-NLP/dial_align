#! /bin/bash -l

#SBATCH -J eflomalpriors
#SBATCH -o log_eflomalpriors.%j.out
#SBATCH -e log_eflomalpriors.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 24:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-efmaral

DATADIR=../../data

set -e

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	cat $DATADIR/$PROJECT/*.orig > $PROJECT"_all".orig
	cat $DATADIR/$PROJECT/*.norm > $PROJECT"_all".norm
	cat ../eflomal/$PROJECT/*.sym > $PROJECT"_all".sym
	python ../mergefiles.py $PROJECT"_all".orig $PROJECT"_all".norm > $PROJECT"_all".text
	makepriors.py -i $PROJECT"_all".text -f $PROJECT"_all".sym -r $PROJECT"_all".sym -p $PROJECT"_all".priors
	mkdir -p $PROJECT

	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		align_eflomal.py -s $DATADIR/$PROJECT/$FID".orig" -t $DATADIR/$PROJECT/$FID".norm" -f $PROJECT/$FID".fwd" -r $PROJECT/$FID".rev" --priors "$PROJECT_all".priors
		atools -c grow-diag-final-and -i $PROJECT/$FID".fwd" -j $PROJECT/$FID".rev" > $PROJECT/$FID".sym"
	done
	rm *_all.orig *_all.norm *_all.sym *_all.text
done
