import shutil
import os
import pandas
import argparse
from pathlib import Path

def args():
    parser = argparse.ArgumentParser(description='Rename MSAs and Split Jobs')
    parser.add_argument('model_folder', type=str, help='path to MSA folder')
    args = parser.parse_args()
    return args

def main(model_folder):
    model_folder_path = Path(model_folder)
    print(model_folder_path)
    current_directory = model_folder_path.parent
    new_folder = "combined_models"
    new_folder_path = current_directory / new_folder

    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)

    for folder in model_folder_path.iterdir():
        if folder.is_dir():
            for file in folder.iterdir():
                if file.is_file() and ("_relaxed_" in file.name or "_scores_" in file.name):
                    new_file_path = new_folder_path / file.name
                    shutil.copy(src = str(file), dst = str(new_file_path))
                    print(f"{new_file_path}")



if __name__ == '__main__':
    args = args()
    model_folder = args.model_folder
    main(model_folder)