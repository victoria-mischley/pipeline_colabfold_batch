#!/bin/bash
#BATCH -J af2_job
#SBATCH -o my_prefix_output.%j.output
#SBATCH -e my_prefix_error.%j.err
#SBATCH -p compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH -t 48:00:00
#SBATCH --account=was138
#SBATCH --mem=220G
______________________________________________________________________


cp -r ~/mmseqs /scratch/$USER/job_$SLURM_JOBID
mkdir test_models_MSA
cp -r test_models_MSA /scratch/$USER/job_$SLURM_JOBID
cp test_models.fasta /scratch/$USER/job_$SLURM_JOBID
cd /scratch/$USER/job_$SLURM_JOBID
mkdir database
cp /expanse/projects/qstore/data/colabfold/database/*index* database
cd database
for JJ in `ls /expanse/projects/qstore/data/colabfold/database | grep -v index`; do ln -s /expanse/projects/qstore/data/colabfold/database/$JJ .; done

cd /scratch/$USER/job_$SLURM_JOBID
timeout 48h colabfold_search test_models.fasta /scratch/$USER/job_$SLURM_JOBID/database test_models_MSA  --mmseqs /home/vmischley/mmseqs/bin/mmseqs --db1 uniref30_2103_db --threads 64 --db-load-mode 0

cp -r test_models_MSA  $SLURM_SUBMIT_DIR
