cwlVersion: v1.2
class: FEMWorkflow

id: nnunet-pancreas-tumour-workflow
label: nnU-Net Pancreas Tumour Workflow
doc: Runs GPU-backed nnU-Net Pancreas Tumour at one selected execution site.

execution_sites:
  - alias: execution_site
    kind: single
    selection: user
    value: null
    doc: Site with a CUDA-capable GPU where the segmentation is executed.

bundles:
  - bundle_id: nnunet-pancreas-tumour-bundle
    doc: Executes nnU-Net Pancreas Tumour.
    site_bindings:
      - role: worker
        site: execution_site

inputs:
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
    scope: global
    constraints: {}
    targets:
      - bundle_id: nnunet-pancreas-tumour-bundle
        bundle_input_name: dicom_series

outputs:
  - id: segmentations
    type: Directory
    doc: Directory containing the generated DICOM SEG files.
    source:
      bundle_id: nnunet-pancreas-tumour-bundle
      bundle_output_name: segmentations

connections: []

metadata:
  author: German Cancer Research Center (DKFZ)
  version: "1.0"
  apps: {}
  version_control:
    repository: "https://github.com/MIC-DKFZ/nnunet-eucaim-docker"
    branch: "main"
    commit: "084b4f1371869b3cc8eeda7d60e14d3d613b5f2a"
    tag: "1.0.0"
  compliance:
    data_classification: private
    retention_policy:
      inputs_retention: Platform policy
      outputs_retention: Platform policy
      logs_retention: Platform policy
    security:
      access_control: []
