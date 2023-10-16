# pipeline_colabfold_batch
python scripts to rename MSA files, divide into jobs, and create submit scripts to run CFB on a cluster. After jobs are finished, script to move all pdb and json files into folder

Before MSA_generation:
- CFS_submit_script.slurm: this is an example submit script for generating the MSA files from a .fasta file. 

Scripts for after MSA generation, but before running Colabfold Batch to generate the models:
- rename_MSAs.py: After running colabfold search, the MSAs are automatically renamed starting at 0.a3m, 1.a3m. etc. This script renames the files back to the name that you gave in the fasta file. This script will put the renamed MSAs into a new folder
- split_msas.py: This script splits all of the MSA files (.a3m files) into groups of MSA files that will in total take ~48 hours to complete. This script will generate a new folder "MSA_jobs" that will contain subdirectories each with the approporiate number MSAs based on sequence length. Each of these folders will correspond to a job to submit to the cluster. 
- gen_CFB_submit_script.py: this script will generate a submit script for each job.
- run_batch_pipeline.py: This script runs rename_MSAs.py,  split_msas.py, gen_CFB_submit_script.py at once. 

Scripts for after the models are finished:
- move_af_files.py: this script moves all of the relevant files from each of the individual job folders to one folder, which can then be downloads/ used to run downstream analysis (ie PPIscreenML).
  
