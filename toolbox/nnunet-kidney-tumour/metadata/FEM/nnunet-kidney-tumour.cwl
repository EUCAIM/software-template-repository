cwlVersion: v1.2
class: FEMTask

id: nnunet-kidney-tumour
label: nnU-Net Kidney Tumour
doc: Segments kidney, tumour, and cyst from DICOM series using nnU-Net Task135_KiTS2021.

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/nnunet-kidney-tumour:1.0.0
  - class: EnvVarRequirement
    envDef:
      - envName: nnUNet_input
        envValue: $(inputs.dicom_series.path)
      - envName: nnUNet_output
        envValue: $(runtime.outdir)
  - class: CUDARequirement
    cudaVersionMin: "11.8"
    cudaDeviceCountMin: 1

baseCommand: [/bin/bash, /app/start_nnunet.sh]

inputs:
  - id: dicom_series
    type: Directory
    doc: Directory whose immediate child directories each contain one DICOM series.
    required: true
    default: null
    hidden: false
    source: user

outputs:
  - id: segmentations
    type: Directory
    doc: Output directory containing generated DICOM SEG files.
    outputBinding:
      glob: .

expectedExitCode: 0

metadata:
  author: German Cancer Research Center (DKFZ)
  version: "1.0"
  orchestrator:
    network: overlay
    additional_metadata:
      model_task: Task135_KiTS2021
      gpu_required: true
