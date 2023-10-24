import os
import shutil
import argparse
from pathlib import Path

def args():
    parser = argparse.ArgumentParser(description='Rename MSAs and Split Jobs')

    parser.add_argument('MSA_folder', type=str, help='path to MSA folder')

    # Parse the command line arguments
    args = parser.parse_args()
    return args

# Assign variables based on command line arguments

#####################################################################################################################################################
def main(MSA_folder):
    MSA_folder_path = Path(MSA_folder)
    MSA_folder = MSA_folder_path.name
    parent_directory = MSA_folder_path.parent
    renamed_MSA_folder = f"{MSA_folder}_renamed"

    renamed_MSA_folder_path = parent_directory / renamed_MSA_folder


    if not os.path.exists(renamed_MSA_folder_path):
        os.mkdir(renamed_MSA_folder_path)

    for file in MSA_folder_path.iterdir():
        file_path = MSA_folder_path / file
        
        with open(file_path, "r") as f:
            # Skip the first line
            f.readline()
            
            # Read the second line
            line = f.readline()
            
        parts = line.split()
        desired_part = parts[0][1:]
        new_name = f"{desired_part}.a3m"
        new_file_location = renamed_MSA_folder_path / new_name
        
        shutil.copy(file_path, new_file_location)

    
if __name__ == '__main__':
    args = args()
    MSA_folder = args.MSA_folder
    main(MSA_folder)
