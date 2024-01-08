# Import necessary modules
import os
import argparse
from pathlib import Path

def args():
    parser = argparse.ArgumentParser(description='Rename MSAs and Split Jobs')

    parser.add_argument('name_of_fasta_file', type=str, help='path to MSA folder')
    parser.add_argument('number_of_recycles', type=str, help='number_of_recycles')
    parser.add_argument('AF_model_version', type=str, help='AF_model_version')
    # Parse the command line arguments
    args = parser.parse_args()
    return args

# Assign variables based on command line arguments
#####################################################################################################################################################

# Set the common file name prefix
def main(name_of_fasta_file, number_of_recycles, AF_model_version):
  prefix = "my_prefix"

  # Set the input file names and where you want the submit script for CFS and CFB to be saved#
  fasta_file_path = Path(name_of_fasta_file)
  print(fasta_file_path)
  parent_directory = fasta_file_path.parent
  print(parent_directory)
  fasta_folder = "fasta_files"
  job_folder = parent_directory / fasta_folder
  print(job_folder)
  
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
    if file != ".DS_Store":
        print(file)
        file_name = file.name[:-6]
        print(file_name)
        job_num = file_name.split("_")[-1]

    ###Write the CFB_script
        output_file_CFB = (f"{model_folder}/{job_num}_CFB_{file_name}_submit.slurm")
        # print(output_file_CFB)

        with open(f"{output_file_CFB}", "w") as f:
            f.write("#!/bin/bash\n#BATCH -J af2_job\n")
            f.write(f"#SBATCH -o {prefix}_output.%j.output\n")
            f.write(f"#SBATCH -e {prefix}_error.%j.err\n") 
            f.write(f"#SBATCH -p {partition_CFB}\n#SBATCH --gpus=1\n#SBATCH --nodes=1\n#SBATCH --ntasks-per-node=1\n")
            f.write(f"#SBATCH -t {time_CFB}\n")
            f.write(f"#SBATCH --account=was136\n#SBATCH --mem={memory}\n")
            f.write("______________________________________________________________________\n")
            f.write("module reset\n\n")
            f.write(f"colabfold_batch {file} {file_name}_models  --model-type {AF_model_version}  --num-recycle {recycles} --amber --use-gpu-relax")
      


if __name__ == '__main__':
    args = args()
    number_of_recycles = args.number_of_recycles
    AF_model_version = args.AF_model_version

    name_of_fasta_file = args.name_of_fasta_file

    if name_of_fasta_file[-6:] == ".fasta":
        final_fasta_file_name = name_of_fasta_file
    else:
        final_fasta_file_name = f"{name_of_fasta_file}.fasta"
    fasta_file_folder = "fasta_files"

    main(name_of_fasta_file, number_of_recycles, AF_model_version)




