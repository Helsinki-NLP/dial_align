#! /bin/bash -l

#SBATCH -J phrextract
#SBATCH -o log_phrextract.%j.out
#SBATCH -e log_phrextract.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 2:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-moses

#ALIGNER=giza
#ALIGNEXT=sym
ALIGNER=levenshtein
ALIGNEXT=fwd+dtw

for PROJECT in archimob ndc skn; do
	echo $ALIGNER $PROJECT
	mkdir -p $ALIGNER/$PROJECT
	FILES=`ls ../$ALIGNER/$PROJECT/*.$ALIGNEXT`
	for F in $FILES; do
		FID=`basename $F .$ALIGNEXT`
	 	echo "  $FID"
		source extract_moses.sh $PROJECT $FID $ALIGNER $ALIGNEXT 4
		rm -f $ALIGNER/$PROJECT/$FID.extract.* $ALIGNER/$PROJECT/$FID.lex.* 
	done
done
