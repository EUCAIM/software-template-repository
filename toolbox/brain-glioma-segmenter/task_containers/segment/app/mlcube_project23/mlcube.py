"""MLCube handler file"""
import typer
import yaml
import os
from os import listdir
from os.path import join
from infer_low_disk import convert_data_step, perform_inference_step, ensemble_step, thresholding_step, convert_back_BraTS_step

app = typer.Typer()

@app.command("infer")
def infer(
    data_path: str = typer.Option(..., "--data_path"),
    output_path: str = typer.Option(..., "--output_path"),
):
    
    # Setting the path for the weights
    os.environ['nnUNet_results'] = '/mlcube_project/checkpoints'
    os.environ['nnUNet_preprocessed'] = 'NONE'
    os.environ['nnUNet_raw'] = 'NONE'
    
    # First step - Convert dataset from BraTS2023 to nnUNet format
    print("Doing first step")
    input_folder_nnunet = 'converted_dataset/'
    convert_data_step(input_folder_nnunet=input_folder_nnunet, raw_dataset=data_path)
    print(f"Number of files in input_folder_nnunet: {len(listdir(input_folder_nnunet))}")

    # Second step - Performing inference for each model
    print("Doing second step")
    inference_folder =  "inference/"
    perform_inference_step(inference_folder=inference_folder, input_folder_nnunet=input_folder_nnunet)
    
    # Third step - Doing the ensemble
    print("Doing third step")
    ensemble_code = 'GB_GL_GS_RB_RL_RS_rGB_rGL_rGS'
    ensemble_step(ensemble_code=ensemble_code, inference_folder=inference_folder) # This function is ignored in the low disk step

    # Fourth step - Thresholding
    print("Doing fourth step")
    min_volume_threshold_WT = 250
    min_volume_threshold_TC = 150
    min_volume_threshold_ET = 100
    thresholding_step(
        min_volume_threshold_WT=min_volume_threshold_WT, 
        min_volume_threshold_TC=min_volume_threshold_TC, 
        min_volume_threshold_ET=min_volume_threshold_ET,
        inference_folder=inference_folder,
        ensemble_code=ensemble_code
        )

    # Fifth step - Converting back from nnUnet to BraTS2023
    print("Doing fifth step")
    convert_back_BraTS_step(
        min_volume_threshold_WT=min_volume_threshold_WT, 
        min_volume_threshold_TC=min_volume_threshold_TC, 
        min_volume_threshold_ET=min_volume_threshold_ET, 
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


