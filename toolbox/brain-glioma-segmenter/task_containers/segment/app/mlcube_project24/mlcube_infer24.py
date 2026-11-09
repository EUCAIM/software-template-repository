"""MLCube handler file"""
import tempfile
import os
from os import listdir
from pathlib import Path

from infer_low_disk_glioma_mednext import convert_data_step, perform_inference_step, thresholding_step, convert_back_BraTS_step
from fops.load_store import maybe_make_dir
from pp_radiomics.feature_extraction import process_case
from pp_cluster.infer import get_cluster, get_cluster_artifacts
from postproc.pp_cc import remove_small_component
from postproc.pp_lblredef import label_redefinition
import shutil
import pandas as pd
from default_mask.masking import apply_default_mask
import nibabel as nib
import numpy as np

def postprocess_single(input_dir, seg_dir, out_dir):
    TASK = 'BraTS-GLI-POST'
    THRESHOLD_FILE_CC = '/mlcube_project/postproc/cc_thresholds_cv.json'
    THRESHOLD_FILE_LBLDEF = '/mlcube_project/postproc/lblredef_thresholds_cv.json'
    case_name = input_dir.name
    CLUSTER_ARTIFACT = get_cluster_artifacts('GLI-POST')
    # create dilated (or not) segmentation on the largest region
    #seg_path = seg_dir / f"{case_name}.nii.gz"
    out_path = maybe_make_dir(out_dir) / f"{case_name}.nii.gz"

    # compute radiomics
    sequences = ['-t1n', '-t1c', '-t2w', '-t2f'] if TASK != 'MEN-RT' else ['_t1c']
    features = process_case(
        case=case_name,
        paramfile="/mlcube_project/pp_radiomics/params.yaml",
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
        remove_small_component(TASK, THRESHOLD_FILE_CC, seg_dir, df_radiomics, out_dir)
        return out_path
    remove_small_component(TASK, THRESHOLD_FILE_CC, seg_dir, df_radiomics, removed_cc_dir)
    # label redefinition
    print(f"Redefining labels for {case_name} task {TASK}")
    label_redefinition(TASK, THRESHOLD_FILE_LBLDEF, removed_cc_dir,df_radiomics, out_dir)
    return out_path

def infer(
    data_path,
    output_path,
):
    # Setting the path for the weights
    os.environ['nnUNet_results'] = '/mlcube_inferer/checkpoints'
    os.environ['RESULTS_FOLDER'] = "/mlcube_inferer/checkpoints"
    #os.environ['nnUNet_preprocessed'] = 'NONE'
    #os.environ['nnUNet_raw'] = 'NONE'
    #os.environ['nnUNet_raw_data_base'] = 'NONE'
    #os.environ['nnUNet_preprocessed'] = 'NONE'

    data_path = Path(data_path)
    output_file = Path(output_path) / f'{data_path.name}.nii.gz'
    one_image = list(data_path.glob('*.nii.gz'))[0]
    
    # First step - Convert dataset from BraTS2023 to nnUNet format
    try:

        with tempfile.TemporaryDirectory() as tmpdirname:

            # First step - Convert dataset from BraTS2024 Glioma to nnUNet format
            print("Doing first step: convert_data_step")
            input_folder_nnunet = os.path.join(tmpdirname, 'converted_dataset/' )#'/mlcube_project/converted_dataset/'
            convert_data_step(input_folder_nnunet=input_folder_nnunet, raw_dataset=data_path)
            print(f"Number of files in input_folder_nnunet: {len(listdir(input_folder_nnunet))}")

            # Second step - Performing inference for each model
            print("Doing second step: perform_inference_step")
            #RNg_RSg_RMg_rGNg_rGSg_rGMg
            ensemble_code = 'RMg_RNg_RSg_rGNg_rGSg_rGMg'
            inference_folder =   os.path.join(tmpdirname, 'inference/' ) #"/mlcube_project/inference/"
            perform_inference_step(inference_folder=inference_folder, input_folder_nnunet=input_folder_nnunet, ensemble_code=ensemble_code)
            print("________________________ Second step completed ________________________")

            # Third step - Doing the ensemble
            print("Doing third step")
            print("Step assemble already done before. skipping")

            # Fourth step - Thresholding
            print("Doing fourth step: thresholding_step")
            min_volume_threshold_WT = 0 # TODO
            min_volume_threshold_TC = 0
            min_volume_threshold_ET = 0
            min_volume_threshold_RC = 0 # TODO
            thresholding_step(
                min_volume_threshold_WT=min_volume_threshold_WT, 
                min_volume_threshold_TC=min_volume_threshold_TC, 
                min_volume_threshold_ET=min_volume_threshold_ET,
                min_volume_threshold_RC=min_volume_threshold_RC,
                inference_folder=inference_folder,
                ensemble_code=ensemble_code
                )

            # Fifth step - Converting back from nnUnet to BraTS2023
            print("Doing fifth step: convert_back_BraTS_step")
            convert_back_BraTS_step(
                min_volume_threshold_WT=min_volume_threshold_WT, 
                min_volume_threshold_TC=min_volume_threshold_TC, 
                min_volume_threshold_ET=min_volume_threshold_ET, 
                min_volume_threshold_RC=min_volume_threshold_RC,
                inference_folder=inference_folder, 
                ensemble_code=ensemble_code,
                brats_final_inference=output_path
                )

            # copy 
            print("Moving results from output path")
            seg_dir = maybe_make_dir(os.path.join(tmpdirname, 'segmentation'))
            # move to segmentation directory
            shutil.move(output_file, seg_dir / f'{data_path.name}.nii.gz')
            try:
                postprocess_single(data_path, seg_dir, output_path)
            except Exception as e:
                print(f"I am panicking! Error during postprocessing: {e}")
                print("Moving unprocessed file to output path")
                shutil.move(seg_dir / f'{data_path.name}.nii.gz', output_file)

            if not os.path.exists(output_file):
                print("segmentation file not found after postprocessing, moving default file")
                apply_default_mask('GLI', str(one_image), str(output_file))
                return
            if (len(np.unique(nib.load(output_file).get_fdata())) < 2):
                print("Found maybe empty segmentation after postprocessing, moving default file")
                apply_default_mask('GLI', str(one_image), str(output_file))
                return
            print("DONE")
            return
    except Exception as e:
        print(f"I am panicking! Error during inference: {e}")
        print("Moving default file to output path")
        apply_default_mask('GLI', str(one_image), str(output_file))
        return