import os
import shutil
import argparse
import numpy as np
from pathlib import Path

def args():
    parser = argparse.ArgumentParser(description='Rename MSAs and Split Jobs')

    parser.add_argument('MSA_folder', type=str, help='path to MSA folder')

    # Parse the command line arguments
    args = parser.parse_args()
    return args

# Assign variables based on command line arguments
#####################################################################################################################################################

def get_sequence_length(MSA_folder_renamed):
    seq_length_dict = {}
    for file in MSA_folder_renamed.iterdir():
        file_path = MSA_folder_renamed / file
        with open(file_path, "r") as f:
            # Skip the first line
            f.readline()
            f.readline()
            sequence = f.readline()
            sequence_length = len(sequence)
            seq_length_dict[file] = sequence_length
            
    return seq_length_dict


def estimate_time(sequence_length):
    est_time = 15.17 * (np.exp(0.0031 * int(sequence_length)))
    return round(est_time * 1.2, 2)


def group_by_time(times, time_limit=2880):
    """Group names by cumulative time."""
    current_time = 0
    group = []
    group_list = []

    for name, time in times.items():
        if current_time + time <= time_limit:
            current_time += time
            group.append(name)
        else:
            group_list.append(group)
            group = [name]
            current_time = time

    if group:
        group_list.append(group)

    return group_list

def main(MSA_folder):
    MSA_folder_path = Path(MSA_folder)
    MSA_folder = MSA_folder_path.name
    parent_directory = MSA_folder_path.parent
    renamed_MSA_folder = f"{MSA_folder}_renamed"
    renamed_MSA_folder_path = parent_directory / renamed_MSA_folder

    seq_length_dict = get_sequence_length(renamed_MSA_folder_path)
    print(seq_length_dict)
    times = {}
    for key in seq_length_dict:
        sequence_length = seq_length_dict[key]
        est_time = estimate_time(sequence_length)
        times[key] = est_time
    print(times)

    group_list = group_by_time(times)
    print(group_list)

    for idx, group in enumerate(group_list, 1):
        folder = "MSA_jobs"
        sub_folder = f"{MSA_folder}_{idx}"
        new_folder = parent_directory / folder / sub_folder
        print(new_folder)
        os.makedirs(new_folder, exist_ok=True)

        for name in group:
            src = renamed_MSA_folder_path / name.name
            dst = new_folder / name.name
            shutil.copy(src, dst)
    

if __name__ == '__main__':
    args = args()
    MSA_folder = args.MSA_folder
    main(MSA_folder)