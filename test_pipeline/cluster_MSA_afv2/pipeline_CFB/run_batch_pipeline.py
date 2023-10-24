import os
import shutil
import argparse
import rename_MSAs
import split_msas
import gen_CFB_submit_script

def args():
    parser = argparse.ArgumentParser(description='Rename MSAs and Split Jobs')

    parser.add_argument('MSA_folder', type=str, help='path to MSA folder')
    parser.add_argument('number_of_recycles', type=str, help='number_of_recycles. Options: 3, 6, 9, 12, 24, 48')
    parser.add_argument('AF_model_version', type=str, help='AF_model_version. Option: alphafold2_ptm, alphafold2_multimer_v1, alphafold2_multimer_v2, alphafold2_multimer_v3')
    # Parse the command line arguments
    args = parser.parse_args()
    return args


def main(MSA_folder_path, number_of_recycles, AF_model_version):
    rename_MSAs.main(MSA_folder_path)
    split_msas.main(MSA_folder_path)
    gen_CFB_submit_script.main(MSA_folder_path, number_of_recycles, AF_model_version)



if __name__ == '__main__':
    args = args()
    MSA_folder_path = args.MSA_folder
    number_of_recycles = args.number_of_recycles
    AF_model_version = args.AF_model_version
    main(MSA_folder_path, number_of_recycles, AF_model_version)
