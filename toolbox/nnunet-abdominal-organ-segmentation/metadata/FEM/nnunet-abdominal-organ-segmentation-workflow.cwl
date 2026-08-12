cwlVersion: v1.2
class: FEMWorkflow

id: nnunet-abdominal-organ-segmentation-workflow
label: nnU-Net Abdominal Organ Segmentation Workflow
doc: Runs GPU-backed nnU-Net Abdominal Organ Segmentation at one selected execution site.

execution_sites:
  - alias: execution_site
    kind: single
    selection: user
    value: null
    doc: Site with a CUDA-capable GPU where the segmentation is executed.

bundles:
  - bundle_id: nnunet-abdominal-organ-segmentation-bundle
    doc: Executes nnU-Net Abdominal Organ Segmentation.
    site_bindings:
      - role: worker
        site: execution_site

inputs:
  - id: dicom_series
    type: Directory
    doc: Directory whose immediate child directories each contain one DICOM series.
    required: true
    default: null
    hidden: false
    scope: global
    constraints: {}
    targets:
      - bundle_id: nnunet-abdominal-organ-segmentation-bundle
        bundle_input_name: dicom_series

outputs:
  - id: segmentations
    type: Directory
    doc: Directory containing the generated DICOM SEG files.
    source:
      bundle_id: nnunet-abdominal-organ-segmentation-bundle
      bundle_output_name: segmentations

connections: []

metadata:
  author: German Cancer Research Center (DKFZ)
  version: "1.0"
  apps: {}
  version_control:
    repository: "https://github.com/MIC-DKFZ/nnunet-eucaim-docker"
    branch: "main"
    commit: "c1bbba939516d0a6c45b89074f018fc5ab566f7d"
    tag: ""
  compliance:
    data_classification: private
    retention_policy:
      inputs_retention: Platform policy
      outputs_retention: Platform policy
      logs_retention: Platform policy
    security:
      access_control: []
