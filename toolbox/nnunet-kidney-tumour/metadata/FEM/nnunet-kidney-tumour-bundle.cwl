cwlVersion: v1.2
class: FEMBundle

id: nnunet-kidney-tumour-bundle
label: nnU-Net Kidney Tumour Bundle
doc: Runs one GPU-backed nnU-Net Kidney Tumour task at a selected site.

mode: standalone

tasks:
  - task_id: nnunet-kidney-tumour
    role: worker
    multiplicity:
      type: single
      doc: One inference task processes the submitted set of DICOM series.

shared_inputs:
  - id: dicom_series
    type: Directory
    doc: Directory whose immediate child directories each contain one DICOM series.
    required: true
    default: null
    hidden: false
    constraints: {}
    targets:
      - task_id: nnunet-kidney-tumour
        task_input_name: dicom_series

shared_outputs:
  - id: segmentations
    type: Directory
    doc: Directory containing the generated DICOM SEG files.
    source:
      task_id: nnunet-kidney-tumour
      task_output_name: segmentations

dependencies: []

metadata:
  author: German Cancer Research Center (DKFZ)
  version: "1.0"
  orchestrator:
    additional_metadata: {}
