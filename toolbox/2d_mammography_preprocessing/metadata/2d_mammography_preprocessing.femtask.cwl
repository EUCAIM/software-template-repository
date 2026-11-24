cwlVersion: v1.2
class: FEMTask

id: 2d_digital_mammography_harmonization
label: Digital Mammography DICOM Preprocessing Tool
doc: >-
  Preprocesses and enhances 2D digital mammography (MG) DICOM images.
  Applies configurable pipelines including z-score normalization, multiple
  denoising methods (adaptive median, gaussian, anisotropic, wavelet, cascade),
  and CLAHE contrast enhancement. CLI arguments take precedence over the optional
  JSON config file, which in turn takes precedence over built-in defaults.

requirements:
  - class: DockerRequirement
    dockerPull: harbor.eucaim.cancerimage.eu/processing-tools/2d_mammography_preprocessing:2.0.0-fem
  
  - class: ResourceRequirement
    coresMin: 4
    ramMin: 8192

baseCommand: [/app/entrypoint.sh]

inputs:
  - id: input_dir
    type: Directory
    doc: >-
      Directory containing the input DICOM files.
    required: true
    hidden: false
    source: user
    inputBinding:
      position: 1
      prefix: --input_dir
      separate: true

  - id: output_dir
    type: string
    doc: >-
      Directory where processed DICOM files are written.
    required: true
    hidden: false
    source: user
    inputBinding:
      position: 2
      prefix: --output_dir
      separate: true
      valueFrom: $(runtime.outdir)

  - id: config_file
    type: File
    doc: >-
      Optional JSON config file. When provided, CLI arguments still take precedence,
      then values from this file, and finally script defaults are used.
    required: false
    hidden: false
    source: user
    inputBinding:
      position: 3
      prefix: --config_file
      separate: true
      valueFrom: $(self.path)

  - id: num_workers
    type: int
    doc: >-
      Number of parallel workers for processing.
    required: false
    hidden: false
    source: user
    inputBinding:
      position: 4
      prefix: --num_workers
      separate: true

  - id: zscore_enabled
    type: string
    doc: >-
      Enable/disable z-score normalization. Script default: true.
    required: false
    hidden: false
    source: user
    constraints:
      enum: ["true", "false"]
    inputBinding:
      position: 5
      prefix: --zscore_enabled
      separate: true

  - id: zscore_p_low
    type: float
    doc: >-
      Lower percentile for clipping (e.g., 1.0). Script default: 1.0.
    required: false
    hidden: false
    source: user
    inputBinding:
      position: 6
      prefix: --zscore_p_low
      separate: true

  - id: zscore_p_high
    type: float
    doc: >-
      Upper percentile for clipping (e.g., 99.0). Script default: 99.0.
    required: false
    hidden: false
    source: user
    inputBinding:
      position: 7
      prefix: --zscore_p_high
      separate: true

  - id: denoise_method
    type: string
    doc: >-
      Denoise algorithm to apply. Script default: cascade.
    required: false
    hidden: false
    source: user
    constraints:
      enum: ["none", "adaptive_median", "gaussian", "anisotropic", "wavelet", "cascade"]
    inputBinding:
      position: 8
      prefix: --denoise_method
      separate: true

  - id: clahe_enabled
    type: string
    doc: >-
      Enable/disable CLAHE (Contrast Limited Adaptive Histogram Equalization).
      Script default: true.
    required: false
    hidden: false
    source: user
    constraints:
      enum: ["true", "false"]
    inputBinding:
      position: 9
      prefix: --clahe_enabled
      separate: true

  - id: clahe_clip_limit
    type: float
    doc: >-
      CLAHE clip limit (typically between 0.005 and 0.02). Script default: 0.01.
    required: false
    hidden: false
    source: user
    inputBinding:
      position: 10
      prefix: --clahe_clip_limit
      separate: true

  - id: series_number
    type: int
    doc: Exact SeriesNumber for processed series. Script default: 2301101.
    required: false
    inputBinding:
      position: 11
      prefix: --series_number
      separate: true

  - id: adaptive_median_ksize
    type: int
    doc: Adaptive median kernel size. Script default: 3.
    required: false
    inputBinding:
      position: 12
      prefix: --adaptive_median_ksize
      separate: true

  - id: gaussian_ksize
    type: int
    doc: Gaussian kernel size. Script default: 3.
    required: false
    inputBinding:
      position: 13
      prefix: --gaussian_ksize
      separate: true

  - id: gaussian_sigma
    type: float
    doc: Gaussian sigma value. Script default: 0.0.
    required: false
    inputBinding:
      position: 14
      prefix: --gaussian_sigma
      separate: true

  - id: anisotropic_niter
    type: int
    doc: Anisotropic diffusion iterations. Script default: 10.
    required: false
    inputBinding:
      position: 15
      prefix: --anisotropic_niter
      separate: true

  - id: anisotropic_kappa
    type: float
    doc: Anisotropic diffusion kappa. Script default: 50.0.
    required: false
    inputBinding:
      position: 16
      prefix: --anisotropic_kappa
      separate: true

  - id: anisotropic_gamma
    type: float
    doc: Anisotropic diffusion gamma. Script default: 0.1.
    required: false
    inputBinding:
      position: 17
      prefix: --anisotropic_gamma
      separate: true

  - id: anisotropic_option
    type: int
    doc: Anisotropic diffusion option (1 or 2). Script default: 1.
    required: false
    inputBinding:
      position: 18
      prefix: --anisotropic_option
      separate: true

  - id: wavelet_wavelet
    type: string
    doc: Wavelet name. Script default: db1.
    required: false
    inputBinding:
      position: 19
      prefix: --wavelet_wavelet
      separate: true

  - id: wavelet_level
    type: int
    doc: Wavelet decomposition level. Script default: 2.
    required: false
    inputBinding:
      position: 20
      prefix: --wavelet_level
      separate: true

  - id: cascade_unsharp_amount
    type: float
    doc: Cascade unsharp amount. Script default: 1.5.
    required: false
    inputBinding:
      position: 21
      prefix: --cascade_unsharp_amount
      separate: true

  - id: cascade_unsharp_sigma
    type: float
    doc: Cascade unsharp sigma. Script default: 1.0.
    required: false
    inputBinding:
      position: 22
      prefix: --cascade_unsharp_sigma
      separate: true

  - id: cascade_gaussian_sigma
    type: float
    doc: Cascade gaussian sigma. Script default: 0.8.
    required: false
    inputBinding:
      position: 23
      prefix: --cascade_gaussian_sigma
      separate: true

  - id: series_description_suffix
    type: string
    doc: >-
      Suffix appended to SeriesDescription to distinguish processed images.
      Script default: _harmonized.
    required: false
    hidden: false
    source: user
    inputBinding:
      position: 24
      prefix: --series_description_suffix
      separate: true

outputs:
  - id: preprocessed_dicoms
    type: Directory
    doc: >-
      Final output directory containing the preprocessed DICOM files maintaining the original structure.
    outputBinding:
      glob: .

expectedExitCode: 0

metadata:
  author: Manuel Marfil-Trujillo / Pedro Miguel Martínez-Gironés / Luis Marti-Bonmati / GIBI230
  version: "2.0.0-fem"
  orchestrator:
    network: overlay
    additional_metadata:
      notes: >-
        Input and output directories are passed as explicit Directory arguments.
        An optional config file can be supplied through --config_file when needed.
        CLI values override JSON values, which in turn override built-in defaults.
        CPU-bound task. Scales well with multiple cores by processing patients in parallel.