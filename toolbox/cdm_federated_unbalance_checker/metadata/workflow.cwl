cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}

inputs:
  dataset_dirs:
    type:
      type: array
      items: Directory

  output_names:
    type:
      type: array
      items: string

outputs:
  report:
    type: File
    outputSource: aggregate/report

steps:
  run_runner:
    run: runner.cwl
    scatter: [dataset_dir, output_name]
    scatterMethod: dotproduct
    in:
      dataset_dir: dataset_dirs
      output_name: output_names
    out: [runner_json]

  aggregate:
    run: aggregator.cwl
    in:
      runner_jsons: run_runner/runner_json
    out: [report]