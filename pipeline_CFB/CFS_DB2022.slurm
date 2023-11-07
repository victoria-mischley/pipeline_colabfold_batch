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
mkdir  MSA_folder_name
cp -r  MSA_folder_name  /scratch/$USER/job_$SLURM_JOBID
cp fasta_file_name.fasta  /scratch/$USER/job_$SLURM_JOBID
cd /scratch/$USER/job_$SLURM_JOBID
mkdir database_2022
cp /expanse/projects/qstore/data/colabfold/database_2022/*index* database_2022
cd database_2022
for JJ in `ls /expanse/projects/qstore/data/colabfold/database_2022 | grep -v index`; do ln -s /expanse/projects/qstore/data/colabfold/database_2022/$JJ .; done

cd /scratch/$USER/job_$SLURM_JOBID
timeout 48h colabfold_search fasta_file_name.fasta /scratch/$USER/job_$SLURM_JOBID/database_2022 MSA_folder_name  --mmseqs /home/vmischley/mmseqs/bin/mmseqs --db1 uniref30_2202_db --threads 64 --db-load-mode 0

cp -r MSA_folder_name  $SLURM_SUBMIT_DIR
