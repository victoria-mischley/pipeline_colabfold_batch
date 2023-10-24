# pipeline_colabfold_batch
There are two different ways to generate models using colabfold batch on expanse:
1. Use the downloaded MSA databases that are on expanse. Run the models using AFV2.
2. Use the online MSA server. Run the models using AFV3.

   The test pipeline folder has example outputs for each method/

# pipeline_CFB:
- this folder only works for MSAs generated on the cluster - 
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


# pipeline_colabfold_batch_onlineMSAgen:
- this folder only works for MSAs generated on the online server. When you run it using the online server, the input is a fasta file and output is the AF model. There is not intermediate step. However, you still need to divide your sequences into jobs that will take 48 hours. However, instead of seperating MSAs this script will seperate the large fasta file into smaller fast files with the appropriate number of sequences.  -
- generate_jobs_onlineMSA.py : this script takes large fasta file and outputs individual fasta files that will take 48 hours. Input is location of fasta file.
-  gen_CFB_submit_script_onlineMSA.py: this script makes a submit script for each of the fasta files that was generated in the previous step.
-  run_pipeline_CFB_onlineMSAgen.py: runs both generate_jobs_onlineMSA.py and gen_CFB_submit_script_onlineMSA.py. This will take the fasta file with all of the sequences, divide them into individual fasta files, and then generatae submit scripts. The input for this script is: location_of_fasta_file, number_of_recycles, version_of_af
    - example submit command: python run_pipeline_CFB_onlineMSAgen.py test_fasta.fasta 12 alphafold2_multimer_v2



#Scripts for after the models are finished:
- move_af_files.py: this script moves all of the relevant files from each of the individual job folders to one folder, which can then be downloaded/ used to run downstream analysis (ie PPIscreenML).

#helpful notes:
- options for version of AF: auto,alphafold2,alphafold2_ptm,alphafold2_multimer_v1,alphafold2_multimer_v2,alphafold2_multimer_v3
