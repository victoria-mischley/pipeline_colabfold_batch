import pandas as pd
import argparse
import os
from pathlib import Path
import gen_CFB_submit_script_onlineMSA
import generate_jobs_onlineMSA


def args():
    parser = argparse.ArgumentParser(description='Rename MSAs and Split Jobs')

    parser.add_argument('name_of_fasta_file', type=str, help='path to MSA folder')
    parser.add_argument('number_of_recycles', type=str, help='number_of_recycles')
    parser.add_argument('AF_model_version', type=str, help='AF_model_version')
    # Parse the command line arguments
    args = parser.parse_args()
    return args

def main(final_fasta_file_name, number_of_recycles, AF_model_version):
    if name_of_fasta_file[-6:] == ".fasta":
        final_fasta_file_name = name_of_fasta_file
    else:
        final_fasta_file_name = f"{name_of_fasta_file}.fasta"

    fasta_file_folder = "fasta_files"
    
    generate_jobs_onlineMSA.main(final_fasta_file_name, fasta_file_folder)

    gen_CFB_submit_script_onlineMSA.main(fasta_file_folder, number_of_recycles, AF_model_version)



if __name__ == '__main__':
    args = args()
    name_of_fasta_file = args.name_of_fasta_file
    number_of_recycles = args.number_of_recycles
    AF_model_version = args.AF_model_version

    if name_of_fasta_file[-6:] == ".fasta":
        final_fasta_file_name = name_of_fasta_file
    else:
        final_fasta_file_name = f"{name_of_fasta_file}.fasta"

    fasta_file_folder = "fasta_files"

    main(final_fasta_file_name, number_of_recycles, AF_model_version)