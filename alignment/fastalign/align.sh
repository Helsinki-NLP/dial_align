#! /bin/bash -l

#SBATCH -J fastal
#SBATCH -o log_fastal.%j.out
#SBATCH -e log_fastal.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 24:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-moses

DATADIR=../../data

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		python ../mergefiles.py $DATADIR/$PROJECT/$FID".orig" $DATADIR/$PROJECT/$FID".norm" > $PROJECT/$FID".text"
		fast_align -i $PROJECT/$FID".text" -d -o -v > $PROJECT/$FID".fwd"
		fast_align -i $PROJECT/$FID".text" -d -o -v -r > $PROJECT/$FID".rev"
		atools -c grow-diag-final-and -i $PROJECT/$FID".fwd" -j $PROJECT/$FID".rev" > $PROJECT/$FID".sym"
	done
done
