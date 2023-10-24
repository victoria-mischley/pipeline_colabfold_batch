# Import necessary modules
import os
import argparse
from pathlib import Path

def args():
    parser = argparse.ArgumentParser(description='Rename MSAs and Split Jobs')

    parser.add_argument('MSA_folder', type=str, help='path to MSA folder')
    parser.add_argument('number_of_recycles', type=str, help='number_of_recycles')
    parser.add_argument('AF_model_version', type=str, help='AF_model_version')
    # Parse the command line arguments
    args = parser.parse_args()
    return args

# Assign variables based on command line arguments
#####################################################################################################################################################

# Set the common file name prefix
def main(MSA_folder, number_of_recycles, AF_model_version):
  prefix = "my_prefix"

  # Set the input file names and where you want the submit script for CFS and CFB to be saved#
  MSA_folder_path = Path(MSA_folder)
  parent_directory = MSA_folder_path.parent
  job_folder_name = "MSA_jobs"
  MSA_folder_path = Path(MSA_folder)
  job_folder = parent_directory / job_folder_name
  model_folder_name = "models"
  model_folder = parent_directory / model_folder_name
  
  if not os.path.exists(model_folder):
     os.mkdir(model_folder)

  partition_CFB = f"gpu-shared"
  time_CFB = f"48:00:00"
  recycles = f"{number_of_recycles}"
  memory = f"90GB"

  files = os.listdir(job_folder)

  for file in job_folder.iterdir():
    file_name = file.name
    job_num = file_name.split("_")[-1]
    print(file_name)
    print(job_num)

  ###Write the CFB_script
    output_file_CFB = (f"{model_folder}/{job_num}_CFB_{file_name}_submit.slurm")
    print(output_file_CFB)

    with open(f"{output_file_CFB}", "w") as f:
      f.write("#!/bin/bash\n#BATCH -J af2_job\n")
      f.write(f"#SBATCH -o {prefix}_output.%j.output\n")
      f.write(f"#SBATCH -e {prefix}_error.%j.err\n") 
      f.write(f"#SBATCH -p {partition_CFB}\n#SBATCH --gpus=1\n#SBATCH --nodes=1\n#SBATCH --ntasks-per-node=1\n")
      f.write(f"#SBATCH -t {time_CFB}\n")
      f.write(f"#SBATCH --account=was138\n#SBATCH --mem={memory}\n")
      f.write("______________________________________________________________________\n")
      f.write("module reset\n\n")
      f.write(f"colabfold_batch {job_folder}/{file_name} {file_name}_models  --model-type {AF_model_version}  --num-recycle {recycles} --amber")
      


if __name__ == '__main__':
    args = args()
    MSA_folder = args.MSA_folder
    number_of_recycles = args.number_of_recycles
    AF_model_version = args.AF_model_version
    main(MSA_folder, number_of_recycles, AF_model_version)




