cwlVersion: v1.2
class: FEMBundle

id: nnunet-brain-tumour-pet-bundle
label: nnU-Net Brain Tumour PET Bundle
doc: Runs one GPU-backed nnU-Net Brain Tumour PET task at a selected site.

mode: standalone

tasks:
  - task_id: nnunet-brain-tumour-pet
    role: worker
    multiplicity:
      type: single
      doc: One inference task processes the submitted set of DICOM series.

shared_inputs:
  - id: dicom_series
    type: Directory
    doc: >-
      Input directory. Accepts either a directory of series subdirectories, or
      the EUCAIM CDM/FS layout
      (dataset/imaging_data/{patient_id}/{study_uid}/{series_uid}/*.dcm).
      Every directory containing .dcm files at any depth is processed as one
      series.
    required: true
    default: null
    hidden: false
    constraints: {}
    targets:
      - task_id: nnunet-brain-tumour-pet
        task_input_name: dicom_series

shared_outputs:
  - id: segmentations
    type: Directory
    doc: Directory containing the generated DICOM SEG files.
    source:
      task_id: nnunet-brain-tumour-pet
      task_output_name: segmentations

dependencies: []

metadata:
  author: German Cancer Research Center (DKFZ)
  version: "1.0"
  orchestrator:
    additional_metadata: {}
