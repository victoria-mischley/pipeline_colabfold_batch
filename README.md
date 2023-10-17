# pipeline_colabfold_batch

#pipeline_CFB:
- this script only works for MSAs generated on the cluster - 
python scripts to rename MSA files, divide into jobs, and create submit scripts to run CFB on a cluster. After jobs are finished, script to move all pdb and json files into folder

Before MSA_generation:
- CFS_submit_script.slurm: this is an example submit script for generating the MSA files from a .fasta file.
  - you need to change the following within the script: MSA_folder_name (this should be the name of the folder that you want the MSAs to be put in), fasta_file_name.fasta (name of fasta file), and location of mmseqs (--mmseqs)

Scripts for after MSA generation, but before running Colabfold Batch to generate the models:
- rename_MSAs.py: After running colabfold search, the MSAs are automatically renamed starting at 0.a3m, 1.a3m. etc. This script renames the files back to the name that you gave in the fasta file. This script will put the renamed MSAs into a new folder
- split_msas.py: This script splits all of the MSA files (.a3m files) into groups of MSA files that will in total take ~48 hours to complete. This script will generate a new folder "MSA_jobs" that will contain subdirectories each with the approporiate number MSAs based on sequence length. Each of these folders will correspond to a job to submit to the cluster. 
- gen_CFB_submit_script.py: this script will generate a submit script for each job.
- run_batch_pipeline.py: This script runs rename_MSAs.py,  split_msas.py, gen_CFB_submit_script.py at once. 

run_batch_pipeline.py takes the following arguments: location of MSA folder (must use full path. ie use pwd and copy that path along with MSA folder name), number of recycles, version of alphafold you wish to use. 
- example submit command: python pipeline_CFB/run_batch_pipeline.py /expanse/lustre/projects/was136/vmischley/vmischley_04_28/test/MSA_files 12 alphafold2_multimer_v2


#pipeline_CFB:
Scripts for after the models are finished:
- move_af_files.py: this script moves all of the relevant files from each of the individual job folders to one folder, which can then be downloaded/ used to run downstream analysis (ie PPIscreenML).

  
