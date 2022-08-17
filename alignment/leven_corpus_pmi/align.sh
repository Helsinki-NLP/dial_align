#! /bin/bash -l

#SBATCH -J levpmi
#SBATCH -o log_levpmi.%j.out
#SBATCH -e log_levpmi.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 24:00:00

module load python-data
source ../pyenv/bin/activate

#for PROJECT in archimob ndc skn; do
for PROJECT in skn; do
	echo $PROJECT
	python3 computeCosts.py $PROJECT levenshtein > $PROJECT.costs
	mkdir -p $PROJECT
	FILES=`ls ../data/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		python3 levalign.py ../data/$PROJECT/$FID".orig" ../data/$PROJECT/$FID".norm" $PROJECT.costs $PROJECT/$FID".fwd"
	done
done

deactivate
