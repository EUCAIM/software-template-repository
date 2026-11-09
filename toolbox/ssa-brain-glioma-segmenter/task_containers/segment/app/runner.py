import tempfile
import os
import shutil
from pathlib import Path
import torch.serialization
torch.serialization.add_safe_globals(["numpy.core.multiarray.scalar"])
from nnunet.install_model import install_model_from_zip
from ensembler.weighted_ensemble import get_ensemble
from nnunet.runner import run_infer_nnunet
from mednext.runner import run_infer_mednext
from pp_cluster.infer import get_cluster, get_cluster_artifacts
from fops.load_store import load_json, maybe_make_dir
from default_mask.masking import apply_default_mask
from pp_radiomics.feature_extraction import process_case#, extract_case
from postproc.pp_cc import remove_small_component
from postproc.pp_lblredef import label_redefinition
import nibabel as nib
import pandas as pd

THRESHOLD_FILE_CC = Path('./postproc/cc_thresholds_cv.json')
THRESHOLD_FILE_LBLDEF = Path('./postproc/lblredef_thresholds_cv.json')

def get_task_config(task):
    year = '2024' if task == 'MEN-RT' else '2025'
    name_mapper = {"_t1c.nii.gz": "_0000.nii.gz"} if task == 'MEN-RT' else load_json(Path('./weights/name.json'))
    return {
        'year': year,
        'name_mapper': name_mapper,
        'nnunet_model_path': f'./weights/BraTS{year}-{task}_nnUNetv2_model.zip',
        'nnunet_resenc_model_path': f'./weights/BraTS2025-{task}_nnUNetv2-ResEnc_model.zip',
        'mednext_model_path': f'weights/BraTS{year}-{task}_MedNeXt_model.zip',
        'ensemble_weights': load_json('./ensembler/weights_cv.json')[task],
        'pyradiomics_paramfile':'./pp_radiomics/params.yaml',
    }

def postprocess_single(input_dir, seg_dir, out_dir):
    case_name = input_dir.name
    # create dilated (or not) segmentation on the largest region
    #seg_path = seg_dir / f"{case_name}.nii.gz"
    out_path = maybe_make_dir(out_dir) / f"{case_name}.nii.gz"

    # compute radiomics
    sequences = ['-t1n', '-t1c', '-t2w', '-t2f'] if TASK != 'MEN-RT' else ['_t1c']
    features = process_case(
        case=case_name,
        paramfile=CONSTANTS['pyradiomics_paramfile'],
        data_path=input_dir.parent,
        seg_dir=seg_dir,
        dilation_factor=None,
        region='wt',
        tmpp='/tmp/',
        seg_suffix='',
        sequences=sequences
    )

    df_radiomics = pd.DataFrame([features])
    # df_radiomics = extract_all(
    #     paramfile = CONSTANTS['pyradiomics_paramfile'],
    #     data_path = input_dir.parent,
    #     seg_dir = seg_dir,
    #     output_path = out_path,
    #     dilation_factor = None,
    #     region = 'wt',
    #     tmpp = '/tmp/',
    #     seg_suffix = '',
    #     sequences = sequences,
    #     max_workers = 1
    # )
    print(f"Radiomics features extracted for {case_name}: {df_radiomics.shape[1]} features")
    print(df_radiomics.head())
    # find cluster
    cluster = get_cluster(df_radiomics, CLUSTER_ARTIFACT)[0]
    df_radiomics['cluster'] = int(cluster)
    print(f"Cluster assignment for {case_name}: {cluster}")
    # remove disconnected regions
    print(f"Removing disconnected regions for {case_name}")
    removed_cc_dir = maybe_make_dir(seg_dir / 'remove_cc')
    if TASK == 'MEN-RT':
        remove_small_component(f"BraTS-{TASK}", THRESHOLD_FILE_CC, seg_dir, df_radiomics, out_dir)
        return out_path
    remove_small_component(f"BraTS-{TASK}", THRESHOLD_FILE_CC, seg_dir, df_radiomics, removed_cc_dir)
    # label redefination
    print(f"Redefining labels for {case_name} task {TASK}")
    label_redefinition(f"BraTS-{TASK}", THRESHOLD_FILE_LBLDEF, removed_cc_dir,df_radiomics, out_dir)
    return out_path

def infer_single(input_path, out_dir):
    """do inference on a single folder

    Args:
        input_path (path): input folder, where the 4 nii.gz are stored
        out_dir (path): out folder, where the seg.nii.gz is to be stored
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_dir = Path(tmpdirname)
        print(f'storing artifacts in tmp dir {temp_dir}')
        input_folder_raw = maybe_make_dir(temp_dir/ 'inp')
        name = input_path.name
        print(name)
        shutil.copytree(input_path, input_folder_raw / name)
        # only for the test
        #os.remove(input_folder_raw / name/ f'{name}-seg.nii.gz')
        for key, val in NAME_MAPPER.items():
            os.rename(input_folder_raw / name/ f'{name}{key}', input_folder_raw / name/ f'{name}{val}')
            one_image = input_folder_raw / name/ f'{name}_0000.nii.gz'
        # apply default mask
        default_mask_path = out_dir / f'{name}.nii.gz'
        apply_default_mask(TASK, str(one_image), str(default_mask_path))

        # run inference
        folds = [0, 1, 2, 3, 4]
        folds_mednext = folds if TASK != 'MEN-RT' else [1, 2, 3, 4]
        try:
            nnunet_npz_path_list = run_infer_nnunet(input_folder_raw/ name, maybe_make_dir(temp_dir/ 'nnunet'), TASK, name, folds=folds)
            nnunet_resenc_npz_path_list = run_infer_nnunet(input_folder_raw/ name, maybe_make_dir(temp_dir/ 'resenc'), TASK, name, folds=folds,resenc=True)
            mednext_npz_path_list, mednext_pkl_path_list = run_infer_mednext(input_folder_raw/ name, maybe_make_dir(temp_dir/ 'mednext'), TASK, name, folds=folds_mednext)
            print(f"nnunet reenc npz files: {nnunet_resenc_npz_path_list}")
            print(f"nnunet npz files: {nnunet_npz_path_list}")
            print(f"mednext npz files: {mednext_npz_path_list}")
            print(f"mednext pkl files: {mednext_pkl_path_list}")
            assert len(nnunet_npz_path_list) == len(nnunet_resenc_npz_path_list), f"Not matching inference lists: {len(nnunet_npz_path_list)}, {len(nnunet_resenc_npz_path_list)}"
        except Exception as e:
            print(f"I am panicking! Error during inference: {e}")
            return
        
        ensemble_folder = maybe_make_dir(input_folder_raw / 'ensemble')
        print(f"Ensembling predictions for {name} in {ensemble_folder}")
        try:
            ensembled_pred_nii_path = get_ensemble(
                nnunet_npz_path_list, 
                nnunet_resenc_npz_path_list, 
                mednext_npz_path_list, 
                mednext_pkl_path_list, 
                ensemble_folder, 
                one_image,
                weights = [
                    ENSEMBLE_WEIGHTS['nnUNetv2'],
                    ENSEMBLE_WEIGHTS['nnUNetv2_ResEnc'],
                    ENSEMBLE_WEIGHTS['MedNeXt'],
                    
                ])
            assert ensembled_pred_nii_path.exists(), f"Ensembled prediction file {ensembled_pred_nii_path} does not exist"
            # check if nonempty
            if nib.load(ensembled_pred_nii_path).get_fdata().sum() < 2:
                raise ValueError(f"Ensembled prediction file {ensembled_pred_nii_path} is empty")
            shutil.copy(ensembled_pred_nii_path, out_dir / f"{name}.nii.gz")
            print(f"Saved ensembled prediction to {out_dir / f'{name}.nii.gz'}")
        except Exception as e:
            print(f"I am panicking! Error during ensembling: {e}")
            return
        
        try:
            radiomics = postprocess_single(input_path, ensemble_folder, out_dir)
        except Exception as e:
            print(f"I am panicking! Error during post processing: {e}")
            return

def batch_processor(input_folder, output_folder):
    for input_path in Path(input_folder).iterdir():
        infer_single(input_path, Path(output_folder))

def setup_model_weights():
    install_model_from_zip(CONSTANTS['nnunet_model_path'])
    install_model_from_zip(CONSTANTS['nnunet_resenc_model_path'])
    install_model_from_zip(CONSTANTS['mednext_model_path'], mednext=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run inference and postprocessing for BraTS2025 tasks.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input folder containing the images.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output folder to store the results.')
    parser.add_argument('-t', '--task', type=str, required=True, help='Task name for which inference is done.')
    args = parser.parse_args()

    print(f"Running inference for task: {args.task}")

    config = get_task_config(args.task)
    global TASK, NAME_MAPPER, ENSEMBLE_WEIGHTS, CONSTANTS, CLUSTER_ARTIFACT
    TASK = args.task
    NAME_MAPPER = config['name_mapper']
    ENSEMBLE_WEIGHTS = config['ensemble_weights']
    CONSTANTS = config
    CLUSTER_ARTIFACT = get_cluster_artifacts(TASK) 

    print(f"Setting up model weights for task: {TASK}")
    #CLUSTER_ARTIFACT = get_cluster_artifacts(TASK)
    setup_model_weights()
    #print(f"Batch processing for task: {TASK}")
    batch_processor(args.input, args.output)