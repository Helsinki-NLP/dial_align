#! /bin/bash -l

#SBATCH -J m2m_121
#SBATCH -o log_m2m121.%j.out
#SBATCH -e log_m2m121.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 10
#SBATCH --mem-per-cpu=1G
#SBATCH -A project_2005047
#SBATCH -t 4:00:00

module load parallel

for PROJECT in archimob ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	ls ../data/$PROJECT/*.orig | parallel -j $SLURM_CPUS_PER_TASK source align_document.sh $PROJECT {}
done
