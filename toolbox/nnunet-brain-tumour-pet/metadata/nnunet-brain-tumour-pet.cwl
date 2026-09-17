cwlVersion: v1.2
class: FEMTask

id: nnunet-brain-tumour-pet
label: nnU-Net Brain Tumour PET
doc: Segments brain tumours from PET imaging from DICOM series using nnU-Net Task169_BrainTumorPET.

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/nnunet-brain-tumour-pet:1.0.0
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
    inputBinding:
      position: 1
      prefix: --input_directory
      separate: true

  - id: output_directory
    type: string
    doc: Directory the DICOM SEG files are written into; FEM supplies its runtime output directory.
    required: true
    default: "."
    hidden: false
    source: user
    inputBinding:
      position: 2
      prefix: --output_directory
      separate: true
      valueFrom: $(runtime.outdir)

outputs:
  - id: segmentations
    type: Directory
    doc: Directory containing the generated DICOM SEG files.
    outputBinding:
      glob: segmentations

expectedExitCode: 0

metadata:
  author: German Cancer Research Center (DKFZ)
  version: "1.0"
  orchestrator:
    network: overlay
    additional_metadata:
      model_task: Task169_BrainTumorPET
      gpu_required: true
