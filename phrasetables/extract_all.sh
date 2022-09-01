#! /bin/bash -l

#SBATCH -J phrextract
#SBATCH -o log.%j.out
#SBATCH -e log.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 6
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 12:00:00

module load parallel

PHRASELEN=4

CONFIGS="giza:sym eflomal:sym fastalign:sym leven:fwd+aai leven_corpus_pmi:fwd+aai m2m_max11_delXY:fwd+aai m2m_max22_delXY_eqmap:fwd"

for CONFIG in $CONFIGS; do
	ARRAY=(${CONFIG//\:/ })
	ALIGNER=${ARRAY[0]}
	ALIGNEXT=${ARRAY[1]}
	echo "Aligner: $ALIGNER  Extension: $ALIGNEXT"
	for PROJECT in archimob ndc skn; do
		echo "  $PROJECT"
		mkdir -p $ALIGNER/$PROJECT
		ls ../alignment/$ALIGNER/$PROJECT/*.$ALIGNEXT | parallel -j $SLURM_CPUS_PER_TASK source extract_moses.sh $PROJECT {} $ALIGNER $ALIGNEXT $PHRASELEN
	done
done
