#! /bin/bash -l

#SBATCH -J eval
#SBATCH -o log_eval.%j.out
#SBATCH -e log_eval.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 6
#SBATCH --mem-per-cpu=1G
#SBATCH -A project_2005047
#SBATCH -t 10:00:00

module load parallel

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh {} "sym" ::: eflomal eflomal_corpus_priors eflomal_leven_priors

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh {} "fwd" ::: m2m_max22 m2m_max22_delXY m2m_max22_delXY_eqmap m2m_max22_eqmap

parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "leven" {} ::: fwd fwd+aai rev rev+aai sym sym+aai

parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh {} "fwd+aai" ::: leven_corpus_pmi leven_doc_pmi leven_swap m2m_max11_delXY m2m_max11_delXY_init