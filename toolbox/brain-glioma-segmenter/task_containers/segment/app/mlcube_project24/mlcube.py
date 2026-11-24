"""MLCube handler file"""
import typer
import yaml
import os
import torch
import os
from os import listdir
from os.path import join
from infer_low_disk_glioma_mednext import convert_data_step, perform_inference_step, thresholding_step, convert_back_BraTS_step


app = typer.Typer()

@app.command("infer")
def infer(
    data_path: str = typer.Option(..., "--data_path"),
    output_path: str = typer.Option(..., "--output_path"),
):
    # Setting the path for the weights
    os.environ['nnUNet_results'] = '/mlcube_project/checkpoints'
    os.environ['RESULTS_FOLDER'] = "/mlcube_project/checkpoints"
    #os.environ['nnUNet_preprocessed'] = 'NONE'
    #os.environ['nnUNet_raw'] = 'NONE'
    #os.environ['nnUNet_raw_data_base'] = 'NONE'
    #os.environ['nnUNet_preprocessed'] = 'NONE'

    if torch.cuda.is_available():
        print("GPU is available")
    else:
        print("GPU is not available")

    # First step - Convert dataset from BraTS2024 Glioma to nnUNet format
    print("Doing first step: convert_data_step")
    input_folder_nnunet = '/mlcube_project/converted_dataset/'
    convert_data_step(input_folder_nnunet=input_folder_nnunet, raw_dataset=data_path)
    print(f"Number of files in input_folder_nnunet: {len(listdir(input_folder_nnunet))}")

    # Second step - Performing inference for each model
    print("Doing second step: perform_inference_step")
    #RNg_RSg_RMg_rGNg_rGSg_rGMg
    ensemble_code = 'RMg_RNg_RSg_rGNg_rGSg_rGMg'
    inference_folder =  "/mlcube_project/inference/"
    perform_inference_step(inference_folder=inference_folder, input_folder_nnunet=input_folder_nnunet, ensemble_code=ensemble_code)
    print("________________________ Second step completed ________________________")

    # Third step - Doing the ensemble
    print("Doing third step")
    print("Step assemble already done before. skipping")

    # Fourth step - Thresholding
    print("Doing fourth step: thresholding_step")
    min_volume_threshold_WT = 50 # TODO
    min_volume_threshold_TC = 0
    min_volume_threshold_ET = 0
    min_volume_threshold_RC = 50 # TODO
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

    print("DONE")




@app.command("hotfix")
def hotfix():
    # NOOP command for typer to behave correctly. DO NOT REMOVE OR MODIFY
    pass

if __name__ == "__main__":
    app()

