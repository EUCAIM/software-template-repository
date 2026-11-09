cwlVersion: v1.2
class: FEMTask

id: brain-metastasis-segmenter
label: Brain Metastasis Segmenter
doc: Neural network-based brain MRI segmentation engine for Brain Metastases (BraTS-MET) on the EUCAIM platform.

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/brain-metastasis-segmenter:v1.0.0
  - class: ResourceRequirement
    coresMin: 4
    ramMin: 16384
  - class: CUDARequirement
    cudaVersionMin: "12.0"
    cudaDeviceCountMin: 1

baseCommand: [python, runner.py]

inputs:
  input_dir:
    type: Directory
    doc: Input directory containing subject MRI folders with NIfTI images (-t1n, -t1c, -t2w, -t2f).
    required: true
    default: null
    hidden: false
    source: user
    inputBinding:
      position: 1
      prefix: -i
      separate: true

  output_dir:
    type: string
    doc: Output directory path where segmentation masks will be generated.
    required: false
    default: "output"
    hidden: true
    source: user
    inputBinding:
      position: 2
      prefix: -o
      separate: true
      valueFrom: $(runtime.outdir)

  task_type:
    type: string
    doc: Task identifier
    required: false
    default: "MET"
    hidden: true
    source: user
    inputBinding:
      position: 3
      prefix: -t
      separate: true

outputs:
  segmentation_masks:
    type: Directory
    doc: Directory containing predicted brain tumor segmentation masks (*.nii.gz).
    outputBinding:
      glob: $(runtime.outdir)

expectedExitCode: 0

metadata:
  author: Biomedical Image Technologies (BIT-UPM) & Pediatric Accelerated Intelligence Lab (Children's National Hospital)
  version: "1.0.0"
  orchestrator:
    network: bridge
    additional_metadata: {}
