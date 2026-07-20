# femtask.schema.yaml
cwlVersion: v1.2
class: FEMTask

id: dicom-deduplication
label: DICOM Deduplication
doc: >
  Scans a DICOM dataset directory and detects duplicate and near-duplicate
  series/instances (exact SOP UID repeats within or across series, hash-identical
  series stored in multiple locations, and pixel-similar near-duplicate series).

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/ingestion-tools/deduplication_tool:latest
  - class: ResourceRequirement
    coresMin: 4
    ramMin: 4096

baseCommand: [python3, dedup_pipeline.py]

inputs:
  dataset_dir:
    type: Directory
    doc: Root directory containing the DICOM dataset to scan (searched recursively).
    required: true
    default: null
    hidden: false
    source: user
    inputBinding:
      position: 1

  workers:
    type: int
    doc: Number of parallel worker processes used for header scanning, hashing, and pixel comparison.
    required: false
    default: 8
    hidden: false
    source: user
    inputBinding:
      position: 2
      prefix: --workers
      separate: true

  exclude_modalities:
    type: string[]
    doc: Modalities to exclude from deduplication analysis (e.g. non-image series such as SEG or RTSTRUCT).
    required: false
    default: ["SEG", "RTSTRUCT"]
    hidden: false
    source: user
    inputBinding:
      position: 3
      prefix: --exclude
      separate: true
      itemSeparator: " "

  sample_step:
    type: int
    doc: Stride used when sampling pixel frames for series hashing (1 = hash every frame).
    required: false
    default: 5
    hidden: false
    source: user
    inputBinding:
      position: 4
      prefix: --sample-step
      separate: true

  keep_nonimage:
    type: boolean
    doc: If set, keep non-image instances instead of filtering them out before comparison.
    required: false
    default: false
    hidden: false
    source: user
    inputBinding:
      position: 5
      prefix: --keep-nonimage

  output_json:
    type: string
    doc: Name of the JSON deduplication report file to be produced.
    required: true
    default: dedup_report.json
    hidden: false
    source: user
    inputBinding:
      position: 6
      prefix: --cache-json
      separate: true
      valueFrom: $(runtime.outdir)/$(self)

outputs:
  dedup_report:
    type: File
    doc: JSON report listing duplicate and near-duplicate findings for the input dataset.
    outputBinding:
      glob: $(inputs.output_json)

expectedExitCode: 0

metadata:
  author: Ioannis Ladakis (iladakig@auth.gr)
  version: "0.9.0"
  orchestrator:
    network: bridge
    additional_metadata: {}
