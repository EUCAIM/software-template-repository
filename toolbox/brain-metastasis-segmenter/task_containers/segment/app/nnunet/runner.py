import subprocess
from tqdm import tqdm
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import math

def maybe_make_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def set_env_paths(input_path: Path) -> str:
    preprocessed = maybe_make_dir(Path('/tmp/nnUNet_preprocessed'))
    return (
        f"nnUNet_raw='{input_path}' "
        f"nnUNet_preprocessed='{preprocessed}' "
        f"nnUNet_results='/tmp/'"
    )

def get_dataset_info(challenge_name: str) -> str:
    dataset_map = {
        "PED": "Dataset041_BraTS2025-PED",
        "MEN-RT": "Dataset024_BraTS2024-MEN-RT",
        "MET": "Dataset040_BraTS2025-MET",
        "MEN": "Dataset042_BraTS2025-MEN"
    }
    if challenge_name not in dataset_map:
        raise ValueError(f"Unsupported challenge name: {challenge_name}")
    return dataset_map[challenge_name]

def run_infer_nnunet(input_folder: str, output_folder: str,  challenge_name: str, name,  folds=[0,1,2,3,4], save_npz=True, resenc=False)->list:
    """_summary_

    Args:
        input_folder (str): input folder
        output_folder (str): folder where output is to be stored
        challenge_name (str): task name for which inference is done
        name (str): file name
        folds (list, optional): describe which folds to run. Defaults to [0,1,2,3,4].
        save_npz (bool, optional): whether to save the probabilities. Defaults to True.

    Returns:
        list: a list of the npz files from each fold
    """
    
    # Check challenge name and get dataset name
    dataset_name = get_dataset_info(challenge_name)
    trainer = "nnUNetTrainer_200epochs"
    configuration = "3d_fullres"
    env_set = set_env_paths(input_folder)
    if resenc:
        dataset_name = "Dataset043_BraTS2025-MEN-RT" if challenge_name == "MEN-RT" else dataset_name
        plans = "nnUNetResEncUNetMPlans"
    else:
        plans = "nnUNetPlans"

    npz_path_list = []
    def run_subprocess_nnunet(fold):
        output_folder_fold = os.path.join(output_folder, f"fold_{fold}")
        print(f"Running nnU-Net inference for fold {fold}")
        cmd = f"{env_set} nnUNetv2_predict -i '{input_folder}' -o '{output_folder_fold}' -d '{dataset_name}' -c '{configuration}' -tr '{trainer}' -p '{plans}' -f '{fold}'"
        if(save_npz):
            cmd+=" --save_probabilities"
        subprocess.run(cmd, shell=True) # Executes the command in the shell
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(run_subprocess_nnunet, folds)
    for fold in tqdm(folds):
        output_folder_fold = os.path.join(output_folder, f"fold_{fold}")
        # Check if the output file exists
        if os.path.exists(os.path.join(output_folder_fold, name+'.npz')):
            npz_path_list.append(Path(os.path.join(output_folder_fold, name+'.npz')))
        else:
            print(f"Segmentation file for fold {fold} not found, skipping.")
            continue
    

    return npz_path_list

 # Executes the command in the shell
