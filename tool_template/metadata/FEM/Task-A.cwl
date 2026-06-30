# femtask.schema.yaml
cwlVersion: v1.2
class: FEMTask # Custom class for FEM, matching cwl’s CommandLineTool

id: string                # Machine-readable name of the task
label: string             # Human-readable name of the task
doc: string               # Description of the task

requirements:
  - class: DockerRequirement
    dockerPull: string    # Full image URL (with tag and pointing to Harbor)
  - class: EnvVarRequirement
    envDef:
      - envName: string   # Any number of environment variables (keep this to minimum and
        envValue: string | expression # stuff that the final user does not need to change)
  - class: ResourceRequirement # Optional
    coresMin: int         # Optional: Minimum CPU cores
    ramMin: int           # Optional: Minimum RAM in MB
  - class: cwltool:CUDARequirement:   # Optional: in case GPU detailed description 
    cudaVersionMin: string            # is required
    cudaComputeCapability: string 
    cudaDeviceCountMin: int   
  - class: InitialWorkDirRequirement: # Optional: mount volumes at runtime 
    listing:                          # (by BSC according  to each node)
      - entryname: string
        entry: string
        writable: boolean # Optional

inputs:
  - input_name: string
    type: string | int | File | Directory | string[]  # Strongly typed
    doc: string
    inputBinding:
      position: int
      prefix: string
      separate: true | false # true: --example VALUE; false: --example=VALUE
      valueFrom: string | expression # Optional

outputs:
  - output_name: string
    type: File | Directory | string[]
    doc: string
    outputBinding:
      glob: string        # Pattern to capture output

baseCommand:
  - string                # Base executable command (array form)

arguments:
  - position: int
    prefix: string
    valueFrom: string | expression # Optional
    separate: true | false # true: --example VALUE; false: --example=VALUE

metadata:                 
  author: string
  version: string
  orchestrator:
    network: overlay | host | bridge
    additional_metadata: object  # Freeform metadata for node-level orchestration
