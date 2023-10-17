import pandas as pd
import argparse
import numpy as np
import os
from pathlib import Path

def args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('name_of_fasta_file', type=str, help = 'name of fasta file with all sequences')
    args = parser.parse_args()
    return args

def get_sequence_length(final_fasta_file_name):
    with open(final_fasta_file_name, "r") as f:
        lines = f.readlines()
        seq_length_dict = {}
        sequence_dict = {}
        for line in lines:
            if line.startswith(">"):
                name = line.strip()[1:]
            else:
                sequence = line.strip()
                sequence_length = len(sequence)
                seq_length_dict[name] = sequence_length
                sequence_dict[name] = sequence
    return seq_length_dict, sequence_dict


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


def main(final_fasta_file_name, fasta_file_folder):
    if not os.path.exists(fasta_file_folder):
        os.mkdir(fasta_file_folder)
    seq_length_dict, sequence_dict = get_sequence_length(final_fasta_file_name)
    times = {}
    for key in seq_length_dict:
        sequence_length = seq_length_dict[key]
        est_time = estimate_time(sequence_length)
        times[key] = est_time
    
    group_list = group_by_time(times)


    for idx, group in enumerate(group_list, 1):
        name_short = final_fasta_file_name[:-6]
        new_fasta_file_name = f"{name_short}_{idx}.fasta"
        folder_path = Path(fasta_file_folder)
        new_file_path = folder_path / new_fasta_file_name
        print(new_file_path)
        newfile = open(new_file_path, "a")
        for name in group:
            if name != ".DS_Store":
                sequence = sequence_dict[name]
                newfile.write(f">{name}" + '\n')
                newfile.write(sequence + '\n')
            
   

if __name__ == '__main__':
    args = args()
    name_of_fasta_file = args.name_of_fasta_file
    if name_of_fasta_file[-6:] == ".fasta":
        final_fasta_file_name = name_of_fasta_file
    else:
        final_fasta_file_name = f"{name_of_fasta_file}.fasta"
    fasta_file_folder = "fasta_files"
    main(final_fasta_file_name, fasta_file_folder)