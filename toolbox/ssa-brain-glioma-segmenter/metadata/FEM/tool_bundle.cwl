cwlVersion: v1.2
class: FEMBundle

id: ssa-brain-glioma-segmenter-bundle
label: Sub-Saharan Africa Brain Glioma Segmenter Bundle
doc: Standalone single-node execution of Sub-Saharan Africa Brain Glioma Segmenter.

mode: standalone

tasks:
  - task_id: ssa-brain-glioma-segmenter
    role: worker
    multiplicity:
      type: single
      doc: Single execution instance of segmentation on the target node.

shared_inputs:
  - id: input_dataset
    type: Directory
    doc: Input directory containing MRI studies formatted according to BraTS / EUCAIM CDM specifications.
    required: true
    default: null
    hidden: false
    targets:
      - task_id: ssa-brain-glioma-segmenter
        task_input_name: input_dir

shared_outputs:
  - id: output_masks
    type: Directory
    doc: Output directory containing predicted segmentation masks.
    source:
      task_id: ssa-brain-glioma-segmenter
      task_output_name: segmentation_masks

dependencies: []

metadata:
  author: Biomedical Image Technologies (BIT-UPM) & Pediatric Accelerated Intelligence Lab (Children's National Hospital)
  version: "1.0.0"
  orchestrator:
    additional_metadata: {}
