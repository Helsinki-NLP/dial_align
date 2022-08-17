#! /bin/bash -l

#SBATCH -J eflomal
#SBATCH -o log_eflomal.%j.out
#SBATCH -e log_eflomal.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 48:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-efmaral

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls ../data/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		align_eflomal.py -s ../data/$PROJECT/$FID".orig" -t ../data/$PROJECT/$FID".norm" -f $PROJECT/$FID".fwd" -r $PROJECT/$FID".rev"
		atools -c grow-diag-final-and -i$PROJECT/$FID".fwd" -j$PROJECT/$FID".rev" > $PROJECT/$FID".sym"
	done
done
