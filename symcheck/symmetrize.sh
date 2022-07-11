#! /bin/bash -l

#SBATCH -J symmetrize
#SBATCH -o log_symmetrize.%j.out
#SBATCH -e log_symmetrize.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 8:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-moses

PROJECT=archimob
ALIGNER=eflomal
mkdir -p $PROJECT

FILES=`ls ../$ALIGNER/$PROJECT/*.fwd`
for F in $FILES; do
	FID=`basename $F .fwd`
	echo "  $FID"
	atools -c grow-diag-final-and -i../$ALIGNER/$PROJECT/$FID.fwd -j../$ALIGNER/$PROJECT/$FID.rev > $PROJECT/$FID.atools
	python3 ../gdfa.py ../data/$PROJECT/$FID.orig ../data/$PROJECT/$FID.norm ../$ALIGNER/$PROJECT/$FID.fwd ../$ALIGNER/$PROJECT/$FID.rev > $PROJECT/$FID.nltk
	python3 ../pharaoh2bal.py ../data/$PROJECT/$FID.orig ../data/$PROJECT/$FID.norm ../$ALIGNER/$PROJECT/$FID.fwd ../$ALIGNER/$PROJECT/$FID.rev > $PROJECT/$FID.bal
	symal -alignment=grow -diagonal=yes -both=yes < $PROJECT/$FID.bal | awk -F' {##} ' '{print $3}' > $PROJECT/$FID.symal
done
