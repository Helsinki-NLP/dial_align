#! /bin/bash -l

#SBATCH -J levalignadj
#SBATCH -o log_levalignadj.%j.out
#SBATCH -e log_levalignadj.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 2:00:00

module use -a /projappl/nlpl/software/modules/etc

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls ../data/$PROJECT/*.orig`

	module load python-data
	source ../pyenv/bin/activate
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		python levalign.py ../data/$PROJECT/$FID".orig" ../data/$PROJECT/$FID".norm" $PROJECT/$FID".fwd" $PROJECT/$FID".rev"
	done
	deactivate

	module load nlpl-efmaral
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  SYM $FID"
		atools -c grow-diag-final-and -i $PROJECT/$FID".fwd" -j $PROJECT/$FID".rev" > $PROJECT/$FID".sym"
	done
done
