cwlVersion: v1.2
class: FEMBundle

id: intracranial-meningioma-segmenter-bundle
label: Intracranial Meningioma Segmenter Bundle
doc: Standalone single-node execution of Intracranial Meningioma Segmenter.

mode: standalone

tasks:
  - task_id: intracranial-meningioma-segmenter
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
      - task_id: intracranial-meningioma-segmenter
        task_input_name: input_dir

shared_outputs:
  - id: output_masks
    type: Directory
    doc: Output directory containing predicted segmentation masks.
    source:
      task_id: intracranial-meningioma-segmenter
      task_output_name: segmentation_masks

dependencies: []

metadata:
  author: Biomedical Image Technologies (BIT-UPM) & Pediatric Accelerated Intelligence Lab (Children's National Hospital)
  version: "1.0.0"
  orchestrator:
    additional_metadata: {}
