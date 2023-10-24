#!/bin/bash
#BATCH -J af2_job
#SBATCH -o my_prefix_output.%j.output
#SBATCH -e my_prefix_error.%j.err
#SBATCH -p gpu-shared
#SBATCH --gpus=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -t 48:00:00
#SBATCH --account=was138
#SBATCH --mem=90GB
______________________________________________________________________
module reset

colabfold_batch /expanse/lustre/projects/was136/vmischley/vmischley_04_28/test_pipeline/online_MSA_afv3/fasta_files/test_models_afv3_1.fasta test_models_afv3_1_models  --model-type alphafold2_multimer_v2  --num-recycle 12 --amber
