#! /bin/bash -l

#SBATCH -J mgiza
#SBATCH -o log_mgiza.%j.out
#SBATCH -e log_mgiza.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 6
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 24:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-moses

NTASKS=6
DATADIR=../../data

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		source align_document.sh $PROJECT $FID $NTASKS >$PROJECT/"$FID.log" 2>&1
		atools -c grow-diag-final-and -i$PROJECT/$FID".fwd" -j$PROJECT/$FID".rev" > $PROJECT/$FID".sym"
	done
done
