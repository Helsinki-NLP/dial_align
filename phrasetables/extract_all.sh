#! /bin/bash -l

#SBATCH -J phrextract
#SBATCH -o log_phrextract.%j.out
#SBATCH -e log_phrextract.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 6
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 2:00:00

module load parallel

PHRASELEN=4
SLURM_CPUS_PER_TASK=5

# ALIGNER=giza
# ALIGNEXT=sym

ALIGNER=leven
ALIGNEXT=fwd+aai

# ALIGNER=eflomal
# ALIGNEXT=sym

for PROJECT in archimob ndc skn; do
	echo $ALIGNER $PROJECT
	mkdir -p $ALIGNER/$PROJECT
	ls ../alignment/$ALIGNER/$PROJECT/*.$ALIGNEXT | parallel -j $SLURM_CPUS_PER_TASK source extract_moses.sh $PROJECT {} $ALIGNER $ALIGNEXT $PHRASELEN
done
