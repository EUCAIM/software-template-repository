cwlVersion: v1.2
class: FEMTask

id: nnunet-colon-cancer
label: nnU-Net Colon Cancer
doc: Segments colon cancer primaries from DICOM series using nnU-Net Task010_Colon.

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/nnunet-colon-cancer:1.0.0
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
      model_task: Task010_Colon
      gpu_required: true
