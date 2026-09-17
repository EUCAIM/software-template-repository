# nnU-Net Brain Tumour PET

This package integrates the nnU-Net v1 model `Task169_BrainTumorPET` into the
EUCAIM platform. It segments brain tumours in a DICOM series and returns a
DICOM SEG object.

The task uses the already registered image:

```text
harbor.eucaim.cancerimage.eu/processing-tools/nnunet-brain-tumour-pet:1.0.0
```

The Dockerfile records the model-specific final image layer. It is built after
the shared `nnunet:base` image in the image-build pipeline; FEM uses the final
Harbor image above.

## Input and output

Provide one directory containing one or more immediate child directories. Each
child directory is processed as one DICOM series:

```text
input/
├── series-1/
│   ├── image-0001.dcm
│   └── image-0002.dcm
└── series-2/
    ├── image-0001.dcm
    └── image-0002.dcm
```

Only files with the lowercase `.dcm` extension are processed. Each series must
contain usable DICOM geometry and enough metadata to construct a DICOM SEG
object.

The task runs on one CUDA-capable GPU. It converts each series to NIfTI, runs
nnU-Net in `3d_fullres` mode, and writes one DICOM SEG file for every non-empty
prediction into a `segmentations/` subdirectory of the output directory, which
is the path the FEM task declares as its output. Output filenames use the
source `SeriesInstanceUID` when available,
or the first DICOM filename as a fallback. The result is exposed as an output
directory.

## FEM metadata

The standalone task, bundle, and workflow are in `metadata/`. The FEM task
preserves the image command (`/bin/bash /app/start_nnunet.sh`) and sets
`nnUNet_input` and `nnUNet_output` to the input directory and FEM runtime
output directory respectively.

## Onboarding test

The required static 18F-FET PET brain-tumour test input is not currently
available as suitable public, redistributable DICOM data. This tool therefore
has no runnable integration fixture; see `test/`.

## Network requirements

### Container execution

No external network access is required during nnU-Net inference.

- Incoming connections: none
- Outgoing connections: none

### Image build

Outbound HTTPS access is required during image build to download dependencies
and pretrained nnU-Net model weights.

### Test data preparation

No test-data downloader is currently provided because a suitable public
18F-FET PET fixture has not yet been identified.

## Hardware requirements

### CPU or GPU

- One NVIDIA GPU is required for inference.
- The GPU must support CUDA 11.8 and be available through the NVIDIA Container
  Toolkit.
- Docker and Podman execution use the GPU through `--gpus all` and
  `nvidia.com/gpu=all`, respectively.
- One GPU is used per container task.
- CPU resources are required for DICOM discovery, DICOM-to-NIfTI conversion,
  preprocessing, postprocessing, and DICOM SEG creation.

### Memory

- GPU memory is used for nnU-Net `3d_fullres` inference and depends on the
  image dimensions and number of slices in the submitted series.
- System memory is used for DICOM data, converted NIfTI volumes, prediction
  arrays, and DICOM SEG generation.
- Peak memory usage depends primarily on the size of the currently processed
  series. Multiple series are processed sequentially.

### Storage

- Persistent storage is required for the input DICOM series and generated
  DICOM SEG files.
- Temporary writable storage is required during execution for DICOM-to-NIfTI
  conversion, nnU-Net preprocessing, prediction files, and postprocessing.
- During image build, additional storage is required for the CUDA base image,
  nnU-Net software, MITK, dependencies, and pretrained model weights.

## Container provenance

`task_containers/brain-pet/dockerfile` records the model-specific image
definition. FEM pulls the registered Harbor image above.

The implementation is maintained in the
[nnUNet EUCAIM Docker repository](https://github.com/MIC-DKFZ/nnunet-eucaim-docker).
The shared base image supplies CUDA 11.8, nnU-Net v1, MITK, and the DICOM/NIfTI
conversion scripts; the task image downloads the pretrained model at build
time.

## License

The container implementation is licensed under Apache-2.0; see `LICENSE`.
Use of the pretrained model weights remains subject to the license and usage
conditions of the dataset on which the model was trained.
